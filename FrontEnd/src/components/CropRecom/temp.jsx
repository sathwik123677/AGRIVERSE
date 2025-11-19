import React ,{useState} from "react";
import axios from "axios";

const CropRecommendation = () => {
  const [form, setForm] = useState({
    temperature: "",
    rainfall: "",
    nitrogen: "",
    phosphorous: "",
    potassium: "",
    ph: "",
    humidity: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const [prediction, setPrediction] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(form);
    const response = await axios.post("http://127.0.0.1:5000", form);

    setPrediction(`The recommended crop is: ${response.data.prediction}`);
  };

  return (
    <div className="flex flex-col items-center justify-center mt-10 md:mt-20">
      <h2 className="text-2xl md:text-4xl mb-5">Crop Recommendation Form</h2>

      <form className="w-full md:max-w-lg bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="temperature"
          >
            Temperature
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            onChange={handleChange}
            value={form.temperature}
            id="temperature"
            type="number"
            placeholder="Temperature"
          />
        </div>

        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="rainfall"
          >
            Rainfall
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            onChange={handleChange}
            value={form.rainfall}
            id="temperature"
            type="number"
            placeholder=" Rainfall"
          />
        </div>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="nitrogen"
          >
            Nitrogen
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            onChange={handleChange}
            value={form.nitrogen}
            id="temperature"
            type="number"
            placeholder=" Nitrogen"
          />
        </div>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="phosphorous"
          >
            Phosphorous
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            onChange={handleChange}
            value={form.phosphorous}
            id="temperature"
            type="number"
            placeholder=" Phosphorous"
          />
        </div>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="potassium"
          >
            Potassium
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            onChange={handleChange}
            value={form.potassium}
            id="temperature"
            type="number"
            placeholder="Potassium"
          />
        </div>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="ph"
          >
            pH
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            onChange={handleChange}
            value={form.ph}
            id="temperature"
            type="number"
            placeholder=" pH"
          />
        </div>
        <div className="flex items-center justify-between">
          <form method ="post" onSubmit={handleSubmit}>
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
            >
              Submit
            </button>
            {prediction && <p>{prediction}</p>}
          </form>
        </div>
      </form>
    </div>
  );
};

export default CropRecommendation;