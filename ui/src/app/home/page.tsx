"use client"

import React, { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';
import Link from "next/link";
import Image from 'next/image';
import { checkLogin, getSessionByID, getSessions } from "@/constants/apiEndpoints"; // Adjust the path as needed

import { Button } from "@/components/ui/button";

import hLogo from '@/../public/humanize_logo.png';

const UserInterface: React.FC = () => {
  const router = useRouter();
  const [username, setUsername] = useState('');

  useEffect(() => {
    checkLogin().then((current_user) => {
      // Do stuff with current user obj, like get username for display
      if (!current_user) {
        router.push("/");
      } else {
        setUsername(current_user.user.username);
      }
    })
  }, []);


  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <Image src={hLogo} alt="Humanize Logo" style={{ width: "150px", marginBottom: "2rem" }} />

      <h1 className="text-[3rem] font-bold m-0">
        Humanize
      </h1>

      <h2 className="text-[1.5rem] font-bold mb-8">
        AI Among Us
      </h2>

      <div className="bg-[#b7fdce] p-8 rounded-[8px] [box-shadow:0_4px_8px_rgba(0,0,0,0.1)] w-[90%] max-w-[400px]">
        <Button asChild className="w-full p-2 mb-5 bg-[#44c4a1] text-[#fff] border-[none] rounded-[4px] cursor-pointer">
        <Link href={{
            pathname: "/play",
            query: { username: username } // Pass username in URL
          }}>
              Play</Link>
        </Button>

        <Button asChild className="w-full p-2 mb-5 bg-[#44c4a1] text-[#fff] border-[none] rounded-[4px] cursor-pointer">
          <Link href="/about">About</Link>
        </Button>

        <Button asChild className="w-full p-2 bg-[#44c4a1] text-[#fff] border-[none] rounded-[4px] cursor-pointer">
          <Link href="/logout">Logout</Link>
        </Button>
      </div>
      
    </div>
  );
}

export default UserInterface
