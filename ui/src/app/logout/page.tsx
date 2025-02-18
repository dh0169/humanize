"use client"

import React from "react";
import { useRouter } from 'next/navigation';
import { API_ENDPOINTS } from "@/constants/apiEndpoints";

import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

const logout: React.FC = () => {
    const router = useRouter();

    const handleLogout = async () => {
        try {
            const res = await fetch(API_ENDPOINTS.AUTH.LOGOUT, {
                credentials: "include",
            });
            const data = await res.json();
            console.log(data);
            router.push("/");
        } catch (error) {
            if(error instanceof Error) {
                console.log(error.message);
            } else {
                console.log("An unknown error occured.");
            }
        }
    };

    handleLogout();
    
    return (
            <div className="flex flex-col items-center justify-center min-h-screen gap-4">
                <Button disabled>
                    <Loader2 className="animate spin" />
                    Logging Out
                </Button>
            </div>
    )

}

export default logout;