
import { BrowserRouter, Routes, Route } from "react-router-dom";

function Home() {
  return <h1 className="text-3xl font-bold">CivicSense Home</h1>;
}

function SinglePrediction() {
  return <h1 className="text-3xl font-bold">Single Prediction</h1>;
}

function BatchPrediction() {
  return <h1 className="text-3xl font-bold">Batch Prediction</h1>;
}

function NotFound() {
  return <h1 className="text-2xl font-bold">404 - Page Not Found</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 p-8 text-white">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<SinglePrediction />} />
          <Route path="/batch-predict" element={<BatchPrediction />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
