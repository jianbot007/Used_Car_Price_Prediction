"use client";
import { useState } from "react";

const conditions = ["new", "like new", "excellent", "good", "fair", "salvage"];
const cylindersOptions = ["3 cylinders", "4 cylinders", "5 cylinders", "6 cylinders", "8 cylinders", "other"];
const fuelOptions = ["gas", "diesel", "electric", "hybrid", "other"];
const titleStatusOptions = ["clean", "salvage", "rebuilt", "lien", "missing", "parts only"];
const transmissionOptions = ["automatic", "manual", "other"];
const driveOptions = ["4wd", "fwd", "rwd"];
const sizeOptions = ["compact", "mid-size", "full-size", "subcompact", "other"];
const typeOptions = ["sedan", "SUV", "truck", "coupe", "convertible", "van", "wagon", "other"];
const paintColorOptions = ["black", "white", "red", "blue", "silver", "green", "yellow", "other"];

export default function UsedCarPricePrediction() {
  const [formData, setFormData] = useState({
    year: "",
    odometer: "",
    manufacturer: "",
    model: "",
    condition: "",
    cylinders: "",
    fuel: "",
    title_status: "",
    transmission: "",
    drive: "",
    size: "",
    type: "",
    paint_color: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setPrediction(data.predicted_price_dollar?.toFixed(2) || "N/A");  // Round to 2 decimals
    } catch (error) {
      console.error("Fetch error:", error);
      setPrediction("Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">
      <div className="bg-gray-800 shadow-lg rounded-2xl p-8 w-full max-w-3xl">
        <h1 className="text-3xl font-bold text-center text-white mb-6">
          🚗 Used Car Price Prediction
        </h1>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <input
            name="year"
            type="number"
            placeholder="Year"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.year}
            onChange={handleChange}
            required
          />
          <input
            name="odometer"
            type="number"
            step="0.1"
            placeholder="Odometer (miles)"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.odometer}
            onChange={handleChange}
            required
          />
          <input
            name="manufacturer"
            placeholder="Manufacturer"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.manufacturer}
            onChange={handleChange}
            required
          />
          <input
            name="model"
            placeholder="Model"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.model}
            onChange={handleChange}
            required
          />

          <select
            name="condition"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.condition}
            onChange={handleChange}
            required
          >
            <option value="">Condition</option>
            {conditions.map((c) => (
              <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
            ))}
          </select>

          <select
            name="cylinders"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.cylinders}
            onChange={handleChange}
            required
          >
            <option value="">Cylinders</option>
            {cylindersOptions.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          <select
            name="fuel"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.fuel}
            onChange={handleChange}
            required
          >
            <option value="">Fuel</option>
            {fuelOptions.map((f) => (
              <option key={f} value={f}>{f.charAt(0).toUpperCase() + f.slice(1)}</option>
            ))}
          </select>

          <select
            name="title_status"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.title_status}
            onChange={handleChange}
            required
          >
            <option value="">Title Status</option>
            {titleStatusOptions.map((t) => (
              <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
            ))}
          </select>

          <select
            name="transmission"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.transmission}
            onChange={handleChange}
            required
          >
            <option value="">Transmission</option>
            {transmissionOptions.map((t) => (
              <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
            ))}
          </select>

          <select
            name="drive"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.drive}
            onChange={handleChange}
            required
          >
            <option value="">Drive</option>
            {driveOptions.map((d) => (
              <option key={d} value={d}>{d.toUpperCase()}</option>
            ))}
          </select>

          <select
            name="size"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.size}
            onChange={handleChange}
            required
          >
            <option value="">Size</option>
            {sizeOptions.map((s) => (
              <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
            ))}
          </select>

          <select
            name="type"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="">Type</option>
            {typeOptions.map((t) => (
              <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
            ))}
          </select>

          <select
            name="paint_color"
            className="p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.paint_color}
            onChange={handleChange}
            required
          >
            <option value="">Paint Color</option>
            {paintColorOptions.map((c) => (
              <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
            ))}
          </select>

          <button
            type="submit"
            className="md:col-span-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
            disabled={loading}
          >
            {loading ? "Predicting..." : "Get Prediction"}
          </button>
        </form>

        {prediction && (
          <div className="mt-6 text-center">
            <p className="text-lg text-gray-300">Estimated Price:</p>
            <p className="text-3xl font-bold text-green-400">${prediction}</p>
          </div>
        )}
      </div>
    </div>
  );
}
