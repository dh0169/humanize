"use client"

import React, { useEffect, useState } from "react";
import ChatComponent from "@/components/wschat";
import { useSearchParams } from 'next/navigation';

const Play: React.FC = () => {
  const searchParams = useSearchParams();
  const [username, setUsername] = useState('');

  useEffect(() => {
    // Get username from URL or session storage
    const urlUsername = searchParams.get('username');
    
    if (urlUsername) {
      setUsername(urlUsername);
    } else {
      // Redirect if no username found
      window.location.href = '/';
    }
  }, [searchParams]);


  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">







      {/* For sake of development, get this flow implemented before next meeting
          TODO: Create function that runs on page load => host room then mounts websocket to that room
          TODO: Refactor ChatComponent to take in roomId as a prop => potential function for random join to find empty/joinable room
          TODO: Connect websocket to stream messages to page 
      */}



      {username && <ChatComponent username={username} />}



    </div>
  )
}

export default Play;
