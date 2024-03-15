"use client";
import Link from "next/link";
import React from "react";

export default function Navbar() {
  return (
    <div
      className="fixed top-0 left-0 h-full bg-gray-900 text-white shadow-md z-50"
      style={{ width: "20%" }}
    >
      <div className="px-4 py-4 flex flex-col">
        <div className="mb-8 flex flex-grow items-center justify-center">
          <h1 className="text-3xl font-bold text-white text-center">
            DEARmandi
          </h1>
        </div>
        <nav className="flex flex-col space-y-4">
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              Home
            </Link>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/home/create_entity"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              Add Kisan Name
            </Link>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/home/inventory"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              Inventory
            </Link>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/home/sales"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              Sales
            </Link>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/home/purchases"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              Purchases
            </Link>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/home/report"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              Report
            </Link>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <Link
              href="/home/faqs"
              className="text-lg hover:text-gray-300 transition-colors duration-300 text-center block"
            >
              FAQs
            </Link>
          </div>
        </nav>
      </div>
    </div>
  );
}
