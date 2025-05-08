// app/play/page.tsx
"use client"

import React, { useEffect, useState } from "react";
import ChatComponent from "@/components/wschat";
import { useSearchParams } from 'next/navigation';
import { API_ENDPOINTS, getSessions } from "@/constants/apiEndpoints";
import { Button } from "@/components/ui/button";

const Play: React.FC = () => {
  const searchParams = useSearchParams();
  const [username, setUsername] = useState('');
  const [roomId, setRoomId] = useState<string>('');
  const [status, setStatus] = useState<'loading' | 'error' | 'ready'>('loading');

  useEffect(() => {
    const urlUsername = searchParams.get('username');
    urlUsername ? setUsername(urlUsername) : window.location.href = '/';
  }, [searchParams]);

  const generateRoomId = () => {
    return Math.random().toString(36).substring(2, 8) + Math.random().toString(36).substring(2, 8);
  };
  
  const handleHostSession = async (): Promise<string> => {
    let attempts = 0;
    const maxAttempts = 5;
    
    while (attempts < maxAttempts) {
      const roomId = generateRoomId();
      const bodyData = { type: "host", room: roomId };
      
      try {
        const res = await fetch(API_ENDPOINTS.LOBBY.BASE, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(bodyData),
          credentials: "include",
        });
        
        const data = await res.json();
        
        if (data.status === "ok") {
          return data.content.room; // Return the successful room ID
        }
        
        if (data.message.includes("room already exists")) {
          attempts++;
          continue;
        }
        
        throw new Error(data.message || "Failed to create room");
      } catch (error) {
        throw new Error((error as Error).message);
      }
    }
    
    throw new Error("Failed to create room after multiple attempts");
  };
  
  // Modified Play page useEffect
  useEffect(() => {
    if (!username) return;
  
    const handleRoomManagement = async () => {
      try {
        // Check existing sessions first
        const sessions = await getSessions();
        const allSessions = [
          ...(sessions.active_sessions || []),
          ...(sessions.pending_sessions || [])
        ];
  
        // Find existing session for user
        const existingSession = allSessions.find(session => 
          session.players.some(player => 
            player.username.trim().toLowerCase() === username.trim().toLowerCase()
          )
        );
  
        if (existingSession) {
          console.log('Found existing session:', existingSession.room);
          setRoomId(existingSession.room);
          setStatus('ready');
          return;
        }
  
        // Attempt to join random room
        const joinResponse = await fetch(API_ENDPOINTS.LOBBY.BASE, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            type: "join",
            random: true,
            room: ""
          }),
        });
  
        const joinData = await joinResponse.json();
        
        if (joinData.status === "ok") {
          console.log('Joined existing room:', joinData.room);
          setRoomId(joinData.room);
          setStatus('ready');
          return;
        }
  
        // Handle specific "already in session" error
        if (joinData.message?.includes("already in a session")) {
          console.log('User already in session - retrieving...');
          const sessions = await getSessions();
          const currentSession = sessions.active_sessions.find(s => 
            s.players.some(p => p.username === username)
          );
          if (currentSession) {
            setRoomId(currentSession.room);
            setStatus('ready');
            return;
          }
        }
  
        // Host new room as fallback
        console.log('Hosting new room...');
        const hostedRoomId = await handleHostSession();
        setRoomId(hostedRoomId);
        setStatus('ready');
        
      } catch (error) {
        console.error('Room management error:', error);
        if (error.message.includes("already in a session")) {
          const sessions = await getSessions();
          const currentSession = sessions.active_sessions.find(s => 
            s.players.some(p => p.username === username)
          );
          if (currentSession) {
            setRoomId(currentSession.room);
            setStatus('ready');
            return;
          }
        }
        setStatus('error');
      }
    };
  
    handleRoomManagement();
  }, [username]);

  if (status === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <h2>Finding or creating a game room...</h2>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <h2 className="text-red-500">Error connecting to game server</h2>
        <Button onClick={() => window.location.reload()}>Retry</Button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      {roomId && <ChatComponent username={username} roomId={roomId} />}
    </div>
  );
}

export default Play;