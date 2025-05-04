import { useEffect, useState, useRef } from "react";
import io, { Socket } from "socket.io-client";
import { v4 as uuidv4 } from "uuid";
import { useRouter } from "next/navigation";

import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { ChatBubble, ChatBubbleMessage } from "@/components/ui/chat/chat-bubble";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { Button } from "@/components/ui/button";
import { CornerDownLeft } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";


// WebSocket connection instance
let socket: typeof Socket | null = null;

interface ChatComponentProps {
  username: string;
  roomId: string;
}


// Type Definitions for Incoming WebSocket Events
interface SessionEvent {
  sessionId: string;
}

interface RoundEvent {
  round: number;
  time: number;
}

interface VoteEvent {
  begin_voting: boolean;
  round: number;
  time: number;
  users: { id: string; username: string }[];
}

interface MessageEvent {
  from: string;
  message: string;
}

interface IncomingMessageEvent {
  from: string;
  message: string;
}

interface ClientMessage extends IncomingMessageEvent {
  id: string;
  timestamp: number;
}

interface JoinEvent {
  room: string;
}



/**
 * ChatComponent - Manages the WebSocket connection for chat functionality.
 */
const ChatComponent: React.FC<ChatComponentProps> = ({ username, roomId }) => {

  const [players, setPlayers] = useState<{ id: string; username: string }[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<string | null>(null);
  const [currentRound, setCurrentRound] = useState<number>(0);
  const [isVotingActive, setIsVotingActive] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState<number>(0);
  const [gameResult, setGameResult] = useState<"human-win" | "ai-win" | null>(null);
  const [messages, setMessages] = useState<ClientMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const router = useRouter();
  const countdownRef = useRef<NodeJS.Timeout | null>(null);

  
  /**
   * Establishes a WebSocket connection and sets up event listeners.
   * @param wsUrl - The WebSocket server URL.
   * @param roomId - The room ID that the user joins.
   * @param username - The username of the current user.
   */
  const setupSocketConnection = (wsUrl: string, roomId: string, username: string): void => {
    if (!username || !roomId) {
      console.error("Missing connection parameters");
      return;
    }
  
    // Updated socket to get rid of error
    socket = io(wsUrl, {
      transports: ["websocket"],
      secure: true,
      transportOptions: {
        websocket: {
          withCredentials: true
        }
      }
    });
  
    // Emit event to join the specified room
    socket.emit("join", { username, room: roomId });
  
    // Handle session start
    socket.on("session_start", (data: SessionEvent) => {
      console.log("Session started:", data);
    });
  
    // Handle session end
    socket.on("session_end", () => {
      socket = null;
      console.log("Session ended!");
    });
  
    // Handle round timer
    const startCountdown = (duration: number) => {
      // Clear existing interval
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
      
      setTimeRemaining(duration);
      
      countdownRef.current = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            clearInterval(countdownRef.current!);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    };
    
    // Handle round start
    socket.on("round_start", (data: RoundEvent) => {
      if (data) {
        console.log(`Round ${data.round} started!`);
        startCountdown(data.time);
      }
    });
    
    // Handle vote phase start
    socket.on("begin_vote", (data: VoteEvent) => {
      if (data) {
        console.log(`Voting started for round ${data.round}`);
        startCountdown(data.time);
        setPlayers(data.users.filter(user => user.username !== username));
        setCurrentRound(data.round);
        setIsVotingActive(true);
        setSelectedPlayer(null);
      }
    });
  
    // Handle round end
    socket.on("round_end", (data: RoundEvent) => {
      if (data) {
        console.log(`Round ${data.round} ended!`);
        setTimeRemaining(0);
        if (countdownRef.current) {
          clearInterval(countdownRef.current);
        }
      }
    });
    
    // Handle vote phase end
    socket.on("stop_vote", (data: RoundEvent) => {
      if (data) {
        console.log(`Voting stopped for round ${data.round}`);
        setTimeRemaining(0);
        setIsVotingActive(false);
        if (countdownRef.current) {
          clearInterval(countdownRef.current);
        }
      }
    });
  
    // Handle user joining the room
    socket.on("join", (data: JoinEvent) => {
      if (data.room) {
        console.log(`Joined room: ${data.room}`);
      }
    });
  
    // Handle chat messages
    socket.on("message", (data: MessageEvent) => {
      if (data) {
        console.log(`${data.from}: ${data.message}`);
      }
    });
  
    // Handle disconnection
    socket.on("disconnect", () => {
      console.log("Socket disconnected");
    });
  };


  
  const handleVote = (playerId: string) => {
    if (!socket || !isVotingActive) return;
    
    setSelectedPlayer(playerId);
    socket.emit("submit_vote", {
      round: currentRound,  // Changed from room to round
      voted_id: playerId
    });
    setIsVotingActive(false);
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  useEffect(() => {
    return () => {
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
    };
  }, []);
  
  


  const wsUrl = "https://humanize.live/chat";




  // Generate unique IDs for messages
  const createClientMessage = (msg: IncomingMessageEvent): ClientMessage => ({
    ...msg,
    id: uuidv4(),
    timestamp: Date.now()
  });

  // Handle incoming messages
  const handleSocketMessages = () => {
    if (!socket) return;

    const messageHandler = (data: IncomingMessageEvent) => {
      if(data.from == username)
        return
      setMessages(prev => [...prev, createClientMessage(data)]);
    };

    socket.on("message", messageHandler);

    return () => {
      socket?.off("message", messageHandler);
    };
  };


  // Send messages with client-generated ID
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim() && socket && username && roomId) {
      const newMessage: ClientMessage = {
        id: uuidv4(),
        from: username,
        message: inputMessage,
        timestamp: Date.now()
      };
  
      // Add optimistically to local state
      setMessages(prev => [...prev, newMessage]);
  
      // Send to server with room parameter - matches debug page format
      socket.emit("message", {
        message: newMessage.message,  // Changed property order to match debug
        room: roomId,                 // Added room parameter
        from: newMessage.from
      });
  
      setInputMessage("");
    }
  };


  useEffect(() => {
    const lastServerMessage = messages
      .filter(msg => msg.from === "Server")
      .pop()?.message;
  
    if (lastServerMessage?.includes("The AI has been identified, Humans win!👩🏻‍🤝‍👨🏾")) {
      setGameResult("human-win");
    } else if (lastServerMessage?.includes("AI Wins 🤖")) {
      setGameResult("ai-win");
    }
  }, [messages]);

  useEffect(() => {
    if (!username || !roomId) return;

    try {
      setupSocketConnection(wsUrl, roomId, username);
      const cleanupMessages = handleSocketMessages();
      
      return () => {
        cleanupMessages?.();
        socket?.disconnect();
        socket = null;
      };
    } catch (error) {
      setConnectionError('Failed to connect to chat server');
    }
  }, [username, roomId]);




  if (connectionError) {
    return (
      <div className="...">
        <h2 className="text-red-500">{connectionError}</h2>
      </div>
    );
  }






  return (
  <div className="relative">
    <div className="absolute top-0 left-1/2 transform -translate-x-1/2 z-10 px-4 py-2 text-3xl font-bold whitespace-nowrap">
      <h1 className="text-3xl font-bold whitespace-nowrap">
        Time remaining: {formatTime(timeRemaining)}
      </h1>
      <h3 className="text-xl text-center mt-2">
        {isVotingActive ? "Vote Phase - Click A Player" : "Chat Phase - Chat With Players"}
      </h3>
    </div>
    

    <div className="flex h-[calc(100vh-200px)] mt-24 ">
      <div className="w-2/3 p-4 text-center flex flex-col h-full bg-[#b7fdce] min-w-[500px] max-w-[500px]">
        <h1 className="m-auto align-middle text-3xl font-bold mb-4">Chat</h1>

        <div className="flex-1 overflow-y-auto mb-4 w-full">
          <ChatMessageList className="flex-1 w-full max-w-full">
            {messages.map((message) => {
              if (message.from === "Server") {
                return (
                  <div key={message.id} className="flex justify-center my-1">
                    <div className="text-gray-500 text-center px-2 space-y-1">
                      <div 
                        className="text-xs [&_h1]:text-lg [&_h1]:font-bold [&_span]:text-muted-foreground"
                        dangerouslySetInnerHTML={{ __html: message.message }}
                      />
                    </div>
                  </div>
                );
              }
              
              return (
                <ChatBubble
                  key={message.id}
                  variant={message.from === username ? 'sent' : 'received'}
                  className="max-w-[80%] mx-auto w-full"
                >
                  <ChatBubbleMessage
                    variant={message.from === username ? 'sent' : 'received'}
                    className="break-words"
                  >
                    {message.message}
                    <div className="text-xs text-muted-foreground mt-1">
                      {message.from}
                    </div>
                  </ChatBubbleMessage>
                </ChatBubble>
              );
            })}
          </ChatMessageList>
        </div>

        <form onSubmit={handleSendMessage} className="mt-4">
          <ChatInput
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message here..."
            className="..."
          />

          <div className="flex items-center p-3 pt-0">
            <Button
              type="submit"
              size="sm"
              className="ml-auto gap-1.5 bg-[#44c4a1]"
            >
              Send Message
              <CornerDownLeft className="size-3.5" />
            </Button>
          </div>
        </form>
      </div>

      <div className="w-1/3 p-4 flex flex-col h-full min-w-[300px]">
        <h1 className="m-auto align-middle text-3xl font-bold mb-4 whitespace-nowrap">
          Players
        </h1>



        <div className="flex-1 overflow-y-auto w-full flex justify-center">
          <div className="flex flex-col items-center gap-2"> {/* Centered items with gap */}
            {players.map((player) => (
              <Button
                key={player.id}
                variant={selectedPlayer === player.id ? "default" : "outline"}
                onClick={() => isVotingActive && handleVote(player.id)}
                className="w-full max-w-[200px] bg-[#44c4a1]"
                disabled={!isVotingActive}
              >
                {player.username}
                {player.username === username && " (You)"}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </div>


    <Dialog open={!!gameResult} onOpenChange={() => setGameResult(null)}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="text-center">
            {gameResult === "human-win" ? "🎉 Humans Win!" : "🤖 AI Dominates!"}
          </DialogTitle>
        </DialogHeader>
        
        <div className="flex flex-col gap-4 py-4">
          <DialogDescription className="text-center text-lg">
            {gameResult === "human-win" 
              ? "Congratulations! You've successfully identified the AI!"
              : "The AI has remained undetected. Better luck next time!"}
          </DialogDescription>
          
          <Button 
            onClick={() => router.push("/home")}
            className="w-full bg-[#44c4a1]"
          >
            Return to Lobby
          </Button>
        </div>
      </DialogContent>
    </Dialog>



  </div>
  );
};

export default ChatComponent;