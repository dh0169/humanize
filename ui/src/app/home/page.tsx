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

      <Button asChild>
      <Link href={{
          pathname: "/play",
          query: { username: username } // Pass username in URL
        }}>
            Play</Link>
      </Button>

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
