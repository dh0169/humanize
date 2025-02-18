"use client"

import React from "react";
 
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import Layout from "@/components/Layout";
import { API_ENDPOINTS } from "@/constants/apiEndpoints";
import { useRouter } from 'next/navigation';

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
        <Layout>
            <Button disabled>
                <Loader2 className="animate spin" />
                Logging Out
            </Button>
        </Layout>
    )

}

export default logout;