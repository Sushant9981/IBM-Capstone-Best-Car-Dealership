import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  const dealer_url = root_url + `djangoapp/dealer/${id}`;
  const review_url = root_url + `djangoapp/add_review`;
  const carmodels_url = root_url + `djangoapp/get_cars`;

  const get_dealer = async () => {
    const res = await fetch(dealer_url, { method: "GET" });
    const data = await res.json();
    if (data.status === 200 && data.dealer.length > 0) {
      setDealer(data.dealer[0]);
    }
  };

  const get_cars = async () => {
    const res = await fetch(carmodels_url, { method: "GET" });
    const data = await res.json();
    setCarmodels(data.CarModels || []);
  };

  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if (name.includes("null")) name = sessionStorage.getItem("username");

    if (!model || !review || !date || !year) {
      alert("All fields are mandatory");
      return;
    }

    const [make, modelName] = model.split(" ");
    const jsoninput = JSON.stringify({
      name,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: make,
      car_model: modelName,
      car_year: year,
    });

    const res = await fetch(review_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsoninput,
    });

    const json = await res.json();
    if (json.status === 200) {
      window.location.href = root_url + "dealer/" + id + "/?refresh=" + new Date().getTime();
    } else {
      alert("Error posting review");
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        <textarea
          id="review"
          cols="50"
          rows="7"
          placeholder="Write your review..."
          onChange={(e) => setReview(e.target.value)}
        />
        <div className="input_field">
          Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>
        <div className="input_field">
          Car Make
          <select onChange={(e) => setModel(e.target.value)}>
            <option value="" disabled selected hidden>
              Choose Car Make and Model
            </option>
            {carmodels.map((carmodel, index) => (
              <option key={index} value={`${carmodel.CarMake} ${carmodel.CarModel}`}>
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>
        <div className="input_field">
          Car Year <input type="number" min="2015" max="2023" onChange={(e) => setYear(e.target.value)} />
        </div>
        <button className="postreview" onClick={postreview}>Post Review</button>
      </div>
    </div>
  );
};

export default PostReview;
