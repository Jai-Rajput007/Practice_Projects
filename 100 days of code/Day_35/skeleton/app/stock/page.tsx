"use client";

import { useState } from "react";
import { Search, TrendingUp, TrendingDown, AlertTriangle, Loader2 } from "lucide-react";

// Define the shape of data coming from FastAPI
interface StockData {
  symbol: string;
  open_price: number;
  high: number;
  low: number;
  price: number;
  volume: number;
  latest_trading_day: string;
  previous_close: number;
  change: number;
  change_percent: string; // Backend sends this as string (e.g. "-1.50%")
}

export default function StockDashboard() {
  const [query, setQuery] = useState("");
  const [stock, setStock] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchStock = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setError("");
    setStock(null);

    try {
      // Call your FastAPI backend
      // Note: Backend appends .BSE, so we just send the name (e.g., RELIANCE)
      const res = await fetch(`http://localhost:8000/stock/${query.trim()}`);

      if (!res.ok) {
        const errData = await res.json();
        // Handle Rate Limiting specifically
        if (res.status === 429) {
          throw new Error("API Limit Reached. Please wait a minute and try again.");
        }
        throw new Error(errData.detail || "Failed to fetch stock data");
      }

      const data: StockData = await res.json();
      setStock(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper to determine if price went up or down
  const isPositive = stock ? stock.change >= 0 : false;

  // Helper to parse the percentage string to a float for the >10% check
  const getChangePercentFloat = (percentStr: string) => {
    return parseFloat(percentStr.replace("%", ""));
  };

  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center p-8">
      <div className="max-w-md w-full">
        {/* Header */}
        <h1 className="text-3xl font-bold text-slate-800 mb-2 text-center">
          BSE Stock Tracker
        </h1>
        <p className="text-slate-500 text-center mb-8">
          Enter a symbol to check price & volatility
        </p>

        {/* Search Form */}
        <form onSubmit={fetchStock} className="relative mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. RELIANCE, TATASTEEL"
            className="w-full p-4 pr-12 rounded-xl border border-slate-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition text-black"
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-3 top-3 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-md">
            <p className="text-red-700 font-medium">Error</p>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Stock Data Card */}
        {stock && (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100 animate-in fade-in slide-in-from-bottom-4 duration-500">
            
            {/* Card Header */}
            <div className="p-6 border-b border-slate-100 flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">{stock.symbol}</h2>
                <p className="text-sm text-slate-500">{stock.latest_trading_day}</p>
              </div>
              <div className={`text-right ${isPositive ? "text-emerald-600" : "text-rose-600"}`}>
                <div className="text-3xl font-bold flex items-center justify-end gap-2">
                  {isPositive ? <TrendingUp className="w-6 h-6" /> : <TrendingDown className="w-6 h-6" />}
                  ₹{stock.price.toFixed(2)}
                </div>
                <div className="font-medium">
                  {isPositive ? "+" : ""}{stock.change} ({stock.change_percent})
                </div>
              </div>
            </div>

            {/* Volatility Alert Logic (> 10%) */}
            {Math.abs(getChangePercentFloat(stock.change_percent)) > 10 && (
              <div className="bg-amber-50 px-6 py-3 border-y border-amber-100 flex items-center gap-3">
                <AlertTriangle className="w-5 h-5 text-amber-600" />
                <div>
                  <p className="text-amber-800 font-bold text-sm">High Volatility Alert</p>
                  <p className="text-amber-700 text-xs">Price changed by more than 10%. News fetching queued.</p>
                </div>
              </div>
            )}

            {/* Grid Stats */}
            <div className="grid grid-cols-2 gap-px bg-slate-100">
              <StatBox label="Open" value={stock.open_price} />
              <StatBox label="Prev Close" value={stock.previous_close} />
              <StatBox label="High" value={stock.high} />
              <StatBox label="Low" value={stock.low} />
              <StatBox label="Volume" value={stock.volume.toLocaleString()} />
              <StatBox label="Change" value={stock.change} color={isPositive ? "text-emerald-600" : "text-rose-600"} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

// Simple sub-component for layout
function StatBox({ label, value, color = "text-slate-800" }: { label: string; value: string | number; color?: string }) {
  return (
    <div className="bg-white p-4">
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-1">{label}</p>
      <p className={`text-lg font-semibold ${color}`}>{value}</p>
    </div>
  );
}