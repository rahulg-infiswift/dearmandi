"use client";

import EntityForm from "@/app/components/CreateEntity";
import Navbar from "@/app/components/Navbar";

export default function CreateEntity() {
  return (
    <div className="flex">
      <Navbar />
      <div className="flex-grow max-w-4xl mx-auto mt-10 px-4 sm:px-6 lg:px-8">
        <EntityForm />
      </div>
    </div>
  );
}
