import { useEffect } from "react";
import io, { Socket } from "socket.io-client";

// WebSocket connection instance
let socket: Socket | null = null;

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
    socket = io(wsUrl, {
        transports: ["websocket"],
        withCredentials: true,
        secure: true,
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
const ChatComponent: React.FC = () => {
    const wsUrl = "/chat";
    const roomId = "room123";
    const username = "player1";

    useEffect(() => {
        // Initialize WebSocket connection
        setupSocketConnection(wsUrl, roomId, username);

        return () => {
            // Cleanup WebSocket connection on component unmount
            if (socket) socket.disconnect();
        };
    }, []);

    return <div>Chat UI</div>;
};

export default ChatComponent;
