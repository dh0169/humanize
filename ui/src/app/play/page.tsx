"use client"

import React from "react";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { ChatBubble, ChatBubbleAvatar, ChatBubbleMessage } from "@/components/ui/chat/chat-bubble";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { Button } from "@/components/ui/button";
import { CornerDownLeft } from "lucide-react";


const Play: React.FC = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen gap-4">
            <h1 className="align-middle text-3xl font-bold">
                Time remaining: 0:00
            </h1>

            <div className="flex">
                <div className="w-1/2 p-4 bg-blue-200 text-center">
                    <h1 className="m-auto align-middle text-3xl font-bold">
                        Chat Box
                    </h1>

                    {/* Wrap with ChatMessageList */}
                    <ChatMessageList>
                        {/* You can map over messages here */}
                        <ChatBubble variant='sent'>
                            <ChatBubbleAvatar fallback='P3' />
                            <ChatBubbleMessage variant='sent'>
                            Hello, how has your day been? I hope you are doing well.
                            </ChatBubbleMessage>
                        </ChatBubble>

                        <ChatBubble variant='received'>
                            <ChatBubbleAvatar fallback='P1' />
                            <ChatBubbleMessage variant='received'>
                            Hi, I am doing well, thank you for asking. How can I help you today?
                            </ChatBubbleMessage>
                        </ChatBubble>

                        <ChatBubble variant='received'>
                            <ChatBubbleAvatar fallback='P5' />
                            <ChatBubbleMessage isLoading />
                        </ChatBubble>
                    </ChatMessageList>
                    
                    <form className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring p-1">
                        <ChatInput
                        placeholder="Type your message here..."
                        className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
                        />

                        <div className="flex items-center p-3 pt-0">
                            <Button
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
        </div>
    )
}

export default Play;