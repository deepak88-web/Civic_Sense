
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import SinglePrediction from "./pages/SinglePrediction";
import BatchPrediction from "./pages/BatchPrediction";
import NotFound from "./pages/NotFound";


function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen flex-col bg-slate-950">

        <Navbar />

        <main className="mx-auto w-full max-w-7xl flex-1 px-6 py-12">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<SinglePrediction />} />
            <Route path="/batch-predict" element={<BatchPrediction />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>

        <Footer />

      </div>
    </BrowserRouter>
  );
}

export default App;
