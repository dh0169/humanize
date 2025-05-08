import React from 'react';
import Image from 'next/image';
import hLogo from '@/../public/humanize_logo.png';

//TODO: Fix the spacing to make it look better, maybe make the text more uniform so it looks better
//TODO: Add a button to go back to the main page

const About: React.FC = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen gap-4 px-4">
            <Image src={hLogo} alt="Humanize Logo" style={{ width: "150px", marginBottom: "2rem" }} />

            <h1 className="text-5xl font-bold m-0">
                Humanize
            </h1>

            <h2 className="text-2xl font-bold mb-8">
                AI Among Us
            </h2>

            <p className="text-center w-1/2 text-3xl italic">
                How To Play:
            </p>
            <div className="w-full max-w-lg text-left space-y-4 mt-4">
                <p><strong>Humanize</strong> is a game which can be explained simply; find the AI Among Us!</p>
                <p>You will be put into a game with 4 other players, but here's the catch: one of them is actually an Artificial Intelligence with the goal of making it to the final round.</p>
                <p>Converse with each other to decipher who is human and who isn't.</p>
                <p>At the end of each round you must choose to vote someone out.</p>
                <p>If the AI gets voted out, the humans win.</p>
                <p>If there is an AI among the last 2 players, the AI wins.</p>
                <p className="font-semibold text-red-600"><strong>Do not let the AI take over humanity!</strong></p>
            </div>
        </div>
    )
}

export default About;