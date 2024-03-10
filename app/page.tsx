import { ArrowRightIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import Image from "next/image";
import SideNav from "./components/sidenav";
import Navbar from "./components/navbar";

export default function Page() {
  return (
    <>
      <Navbar/>
      <div className="max-w-4xl mx-auto mt-10 px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-center mb-6 sm:text-4xl">Welcome to Our Accounting Services</h1>
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2 sm:text-2xl">Inventory Management</h2>
          <p>Efficiently manage your inventory and stock levels.</p>
        </section>
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2 sm:text-2xl">Sales Tracking</h2>
          <p>Keep track of sales performance and metrics.</p>
        </section>
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2 sm:text-2xl">Purchase Orders</h2>
          <p>Manage your purchasing process and supplier interactions.</p>
        </section>
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2 sm:text-2xl">Financial Reports</h2>
          <p>Access comprehensive financial reports for informed decision-making.</p>
        </section>
        <section>
          <h2 className="text-xl font-semibold mb-2 sm:text-2xl">FAQs</h2>
          <p>Find answers to common questions about our accounting services.</p>
        </section>
      </div>
    </>
  );
}
