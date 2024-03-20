"use client";

import CreateEntity from "@/app/components/CreateEntity";
import Navbar from "@/app/components/Navbar";

export default function page() {
  return (
    <div className="flex min-h-screen">
      <Navbar />
      <div className="flex-grow max-w-4xl mx-auto mt-10 px-4 sm:px-6 lg:px-8">
        <CreateEntity />
      </div>
    </div>
  );
}
