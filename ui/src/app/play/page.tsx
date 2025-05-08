'use client'

import React, { Suspense } from 'react';
import PlayInner from './play-inner';

export default function PlayPage() {
  return (
    <Suspense fallback={<div className="flex flex-col items-center justify-center min-h-screen gap-4">Loading...</div>}>
      <PlayInner />
    </Suspense>
  );
}

