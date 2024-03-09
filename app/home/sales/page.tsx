import Link from "next/link";
import Layout from "../../layout";
import Navbar from "@/app/components/navbar";

const Sales = () => (
  <Layout>
    {/* Wrap the navbar and content in a flex container */}
    <div className="flex flex-col md:flex-row min-h-screen">
      {/* Navbar with adjusted styles for mobile */}
      <div className="md:flex-1 md:max-w-xs">
        <Navbar />
      </div>
      {/* Content area */}
      <div className="flex-1 p-4">
        {/* Center the form container on medium and larger screens */}
        <div className="max-w-4xl mx-auto">
          <h1 className="text-center text-2xl font-semibold mb-6">
            Sales Tracking
          </h1>
          <p className="text-center mb-8">
            Monitor sales trends, analyze performance, and identify opportunities
            for growth. Track sales by product, region, or salesperson.
          </p>
          <form className="flex flex-col space-y-4 items-center">
            <div className="w-full max-w-md">
              <label htmlFor="kisanName" className="block font-bold text-xl mb-2">
                Kisan Name
              </label>
              <input
                type="text"
                id="kisanName"
                name="kisanName"
                className="mt-1 w-full px-4 py-2 border rounded-md"
                required
              />
            </div>

            <div className="w-full max-w-md">
              <label htmlFor="cropName" className="block font-bold text-xl mb-2">
                Crop Name
              </label>
              <input
                type="text"
                id="cropName"
                name="cropName"
                className="mt-1 w-full px-4 py-2 border rounded-md"
                required
              />
            </div>

            <div className="w-full max-w-md">
              <label htmlFor="quantity" className="block font-bold text-xl mb-2">
                Quantity
              </label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                className="mt-1 w-full px-4 py-2 border rounded-md"
                required
              />
            </div>

            <div className="w-full max-w-md">
              <label htmlFor="totalWeight" className="block font-bold text-xl mb-2">
                Total Weight
              </label>
              <input
                type="number"
                id="totalWeight"
                name="totalWeight"
                className="mt-1 w-full px-4 py-2 border rounded-md"
                required
              />
            </div>

            <div className="w-full max-w-md">
              <label htmlFor="price" className="block font-bold text-xl mb-2">
                Price
              </label>
              <input
                type="number"
                id="price"
                name="price"
                className="mt-1 w-full px-4 py-2 border rounded-md"
                required
              />
            </div>

            <button
              type="submit"
              className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    </div>
  </Layout>
);

export default Sales;
