"use client"

import React, { useEffect } from "react";
import { API_ENDPOINTS, checkLogin } from "@/constants/apiEndpoints"; // Adjust the path as needed
import Layout from '@/components/Layout';
import { Button } from "@/components/ui/button";

import { useRouter } from 'next/navigation';
import Link from "next/link";

import Image from 'next/image';
import hLogo from '@/../public/humanize_logo.png';

const UserInterface: React.FC = () => {
    const router = useRouter();

    // Also add this to apiEndpoints?
    const handleLogout = async () => {
        try {
          const res = await fetch(API_ENDPOINTS.AUTH.LOGOUT, {
            credentials: "include",
          });
          const data = await res.json();
          console.log(data);
        } catch (error) {
            if(error instanceof Error) {
                console.log(error.message);
            } else {
                console.log("An unknown error occured.");
            }
        }
    };
3
    useEffect(() => {
        checkLogin().then((current_user) => {
          // Do stuff with current user obj, like get username for display
          console.log(current_user) 
          if(!current_user){
            router.push("/");
          }
        })
      });
    

    return (
        <Layout>
            <Image src={hLogo} alt="Humanize Logo" style={{ width: "150px", marginBottom: "2rem" }}/>
            <h1 style={{ fontSize: "3rem", fontWeight: "bold", margin: 0 }}>
                Humanize
            </h1>
            <h2
                style={{
                    fontSize: "1.5rem",
                    fontWeight: "bold",
                    marginBottom: "2rem",
                }}
            >
                AI Among Us
            </h2>

            
            <Button asChild>
                <Link href="/play">Play</Link>
            </Button>
            <Button asChild>
                <Link href="/about">About</Link>
            </Button>
            <Button asChild>
                <Link href="/logout">Logout</Link>
            </Button>
            

        </Layout>
    );
}

export default UserInterface


// <CustBut text="Play" navLoc="/play" />
// <CustBut text="About" navLoc="/about"/>
// <CustBut text="Logout" navLoc="/" onClick={handleLogout}/>