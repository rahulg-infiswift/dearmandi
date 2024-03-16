import Navbar from "@/app/components/Navbar";
import Layout from "../../layout";

const FAQs = () => (
  <div>
    <Navbar />

    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">FAQs</h1>
      <div className="space-y-4">
        <div className="p-4 rounded-lg shadow-md">
          <h2 className="font-semibold text-xl">
            How can I track my inventory levels?
          </h2>
          <p className="mt-2">
            Our inventory management system allows you to monitor stock levels
            in real-time, set up notifications for low stock, and generate
            reports for inventory analysis.
          </p>
        </div>

        <div className="p-4 rounded-lg shadow-md">
          <h2 className="font-semibold text-xl">Can I export sales data?</h2>
          <p className="mt-2">
            Yes, our sales tracking feature includes the ability to export data
            in various formats for further analysis or for use in other business
            applications.
          </p>
        </div>

        <div className="p-4 rounded-lg shadow-md">
          <h2 className="font-semibold text-xl">
            What kind of financial reports can I generate?
          </h2>
          <p className="mt-2">
            You can generate a variety of financial reports, including income
            statements, balance sheets, cash flow statements, and more, to
            understand your business's financial performance.
          </p>
        </div>
      </div>
    </div>
  </div>
);

export default FAQs;
