import { ArrowRightIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import styles from "@/app/components/home.module.css";
import { lusitana } from "@/app/components/fonts";
import Image from "next/image";
import SideNav from "./components/sidenav";

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col p-6">
      <div className="flex flex-col h-10 shrink-0 justify-end rounded-lg bg-blue-500 p-4 md:h-36 text-white text-4xl">
        <div>DEAR Mandi</div>
        <div>Double Entry Accounting and Reporting</div>
      </div>
      <div className="w-full flex-none md:w-64">
        <SideNav />
      </div>
      <h1 className={`${lusitana.className} mb-4 text-xl md:text-2xl`}>
        Dashboard
      </h1>
    </main>
  );
}
