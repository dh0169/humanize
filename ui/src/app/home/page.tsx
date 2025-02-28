"use client"

import React, { useEffect } from "react";
import { useRouter } from 'next/navigation';
import Link from "next/link";
import Image from 'next/image';
import { checkLogin, getSessionByID, getSessions } from "@/constants/apiEndpoints"; // Adjust the path as needed

import { Button } from "@/components/ui/button";
import ChatComponent from "@/components/ui/wschat";

import hLogo from '@/../public/humanize_logo.png';

const UserInterface: React.FC = () => {
    const router = useRouter();
    useEffect(() => {
        checkLogin().then((current_user) => {
            // Do stuff with current user obj, like get username for display
            if(!current_user){
                router.push("/");
            }
        })

        //Prints all sessions
        getSessions().then((current_sessions) => {
            console.log("All sessions:", current_sessions)
        })
    
        
        //Prints game session with id=1
        getSessionByID(1).then((current_session) => {
            console.log("Session with id=1:", current_session)
        }) 
    });
    

    return (
            <div className="flex flex-col items-center justify-center min-h-screen gap-4">
                <Image src={hLogo} alt="Humanize Logo" style={{ width: "150px", marginBottom: "2rem" }}/>

                <h1 className="text-[3rem] font-bold m-0">
                    Humanize
                </h1>

                <h2 className="text-[1.5rem] font-bold mb-8">
                    AI Among Us
                </h2>
                
                <Button asChild>
                    <Link href="/play">Play</Link>
                </Button>

                <ChatComponent>
                    
                </ChatComponent>

                <Button asChild>
                    <Link href="/about">About</Link>
                </Button>
                
                <Button asChild>
                    <Link href="/logout">Logout</Link>
                </Button>
            </div>
    );
}

export default UserInterface