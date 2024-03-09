import Link from "next/link";
import React from "react";

export default function Navbar() {
  return (
    <div className="fixed top-0 left-0 h-full bg-gray-800 text-white p-4">
       <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">DEARmandi</h1>
        <label htmlFor="menu-toggle" className="cursor-pointer lg:hidden block">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M4 6h16M4 12h16m-7 6h7"
            ></path>
          </svg>
        </label>
        <input className="hidden" type="checkbox" id="menu-toggle" />
      </div>
      <nav className="bg-gray-800 text-white p-4">
        <ul className="fflex flex-col space-y-4">
          <li>
            <Link href="/" className="hover:text-gray-300 block">
              Home
            </Link>
          </li>
          <li>
            <Link href="/home/inventory" className="hover:text-gray-300 block">
              Inventory
            </Link>
          </li>
          <li>
            <Link href="/home/sales" className="hover:text-gray-300">
              Sales
            </Link>
          </li>
          <li>
            <Link href="/home/purchases" className="hover:text-gray-300">
              Purchases
            </Link>
          </li>
          <li>
            <Link href="/home/report" className="hover:text-gray-300">
              Report
            </Link>
          </li>
          <li>
            <Link href="/home/faqs" className="hover:text-gray-300">
              FAQs
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
