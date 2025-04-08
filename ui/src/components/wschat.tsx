import { useEffect, useState, useRef } from "react";
import io, { Socket } from "socket.io-client";
import { v4 as uuidv4 } from "uuid";

import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { ChatBubble, ChatBubbleAvatar, ChatBubbleMessage } from "@/components/ui/chat/chat-bubble";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { Button } from "@/components/ui/button";
import { CornerDownLeft } from "lucide-react";




// WebSocket connection instance
let socket: typeof Socket | null = null;

interface ChatComponentProps {
  username: string;
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
  round: number;
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
 * Establishes a WebSocket connection and sets up event listeners.
 * @param wsUrl - The WebSocket server URL.
 * @param roomId - The room ID that the user joins.
 * @param username - The username of the current user.
 */
const setupSocketConnection = (wsUrl: string, roomId: string, username: string): void => {
  /*
  socket = io(wsUrl, {
    transports: ["websocket"],
    withCredentials: true,
    secure: true,
  });
  */

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

  // Handle round start
  socket.on("round_start", (data: RoundEvent) => {
    if (data) {
      console.log(`Round ${data.round} started!`);
      // Trigger UI updates and countdown
    }
  });

  // Handle round end
  socket.on("round_end", (data: RoundEvent) => {
    if (data) {
      console.log(`Round ${data.round} ended!`);
    }
  });

  // Handle voting start
  socket.on("begin_vote", (data: VoteEvent) => {
    if (data) {
      console.log(`Voting started for round ${data.round}`);
      // Display voting options
      data.users.forEach((user) => {
        if (user.username !== username) {
          console.log(`Vote for: ${user.username}`);
          // Attach event listener for vote submission
        }
      });
    }
  });

  // Handle voting stop
  socket.on("stop_vote", (data: RoundEvent) => {
    if (data) {
      console.log(`Voting stopped for round ${data.round}`);
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

/**
 * ChatComponent - Manages the WebSocket connection for chat functionality.
 */
const ChatComponent: React.FC<ChatComponentProps> = ({ username }) => {
  const wsUrl = "humanize.live/api/chat";
  const roomId = "gregtest";

  // State management
  const [messages, setMessages] = useState<ClientMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

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
    if (inputMessage.trim() && socket && username) {
      const newMessage: ClientMessage = {
        id: uuidv4(),
        from: username,
        message: inputMessage,
        timestamp: Date.now()
      };

      // Add optimistically to local state
      setMessages(prev => [...prev, newMessage]);

      // Send to server (without client-generated ID)
      socket.emit("message", {
        from: newMessage.from,
        message: newMessage.message
      });

      setInputMessage("");
    }
  };

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (!username) return; // Add guard clause


    setupSocketConnection(wsUrl, roomId, username);
    const cleanupMessages = handleSocketMessages();

    return () => {
      cleanupMessages?.();
      if (socket) {
        socket.disconnect();
        socket = null;
      }
    };
  }, [username]);



  return <div>
    <h1 className="align-middle text-3xl font-bold">
      Time remaining: 0:00
    </h1>

    <div className="flex">
      <div className="w-1/2 p-4 bg-blue-200 text-center">
        <h1 className="m-auto align-middle text-3xl font-bold">
          Chat Box
        </h1>

        <ChatMessageList>
          {messages.map((message) => (
            <ChatBubble
              key={message.id}
              variant={message.from === username ? 'sent' : 'received'}
            >
              <ChatBubbleAvatar
                fallback={message.from.slice(0, 2).toUpperCase()}
              />
              <ChatBubbleMessage
                variant={message.from === username ? 'sent' : 'received'}
              >
                {message.message}
                <div className="text-xs text-muted-foreground mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </ChatBubbleMessage>
            </ChatBubble>
          ))}
          <div ref={messagesEndRef} />
        </ChatMessageList>

        <form onSubmit={handleSendMessage} className="...">
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
              className="ml-auto gap-1.5"
            >
              Send Message
              <CornerDownLeft className="size-3.5" />
            </Button>
          </div>
        </form>
      </div>

      <div className="w-1/2 p-4 flex flex-col items-center">
        <h1 className="m-auto align-middle text-3xl font-bold">
          Players Remaining
        </h1>




        {/* TODO: Populate players based on info from server*/}
        <Button variant="outline">
          <ChatBubbleAvatar fallback='P1' /> Player 1
        </Button>

        <Button variant="outline">
          <ChatBubbleAvatar fallback='P2' /> Player 2
        </Button>

        <Button variant="outline">
          <ChatBubbleAvatar fallback='P3' /> Player 3 (You)
        </Button>

        <Button variant="outline">
          <ChatBubbleAvatar fallback='P4' /> Player 4
        </Button>

        <Button variant="outline">
          <ChatBubbleAvatar fallback='P5' /> Player 5
        </Button>

        <Button variant="outline">
          <ChatBubbleAvatar fallback='P6' /> Player 6
        </Button>
      </div>
    </div>





    Chat UI
  </div>;
};

export default ChatComponent;
