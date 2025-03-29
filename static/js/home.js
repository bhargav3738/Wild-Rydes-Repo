// document.getElementById("departure").addEventListener("input", fetchFlights);

// function fetchFlights() {
//   const departureCity = document
//     .getElementById("departure")
//     .value.toUpperCase();
//   const url = `http://127.0.0.1:8000/flights/flight/search/?departure_city=${departureCity}`;

//   fetch(url)
//     .then((response) => response.json())
//     .then((data) => {
//       const flightList = document.getElementById("flightList");
//       flightList.innerHTML = ""; // Clear existing list

//       if (data.length === 0) {
//         flightList.innerHTML = "<li>No flights found</li>";
//         return;
//       }

//       // Populate the list with flight data
//       data.forEach((flight) => {
//         const listItem = document.createElement("li");
//         listItem.innerHTML = `
//             <a href="#">
//             <h3>${flight.flight_number}: ${flight.departure_city} to ${
//           flight.arrival_city
//         }</h3>
//             <p>Departure: ${new Date(
//               flight.departure_time
//             ).toLocaleString()}</p>
//             <p>Arrival: ${new Date(flight.arrival_time).toLocaleString()}</p>
//             <p>Price: $${flight.price}</p>
//             <p>Available Seats: ${flight.available_seats}</p>
//             </a>
//         `;
//         flightList.appendChild(listItem);
//       });
//     })
//     .catch((error) => console.error("Error fetching flights:", error));
// }

// function filterDisplayedFlights() {
//   const departureInput = document
//     .getElementById("departure")
//     .value.toUpperCase();
//   const flightList = document.getElementById("flightList");
//   const flights = flightList.getElementsByTagName("li");

//   // Loop through all list items and filter based on input
//   for (let i = 0; i < flights.length; i++) {
//     const flight = flights[i];
//     const txtValue = flight.textContent || flight.innerText;
//     if (txtValue.toUpperCase().includes(input)) {
//       flight.style.display = "";
//     } else {
//       flight.style.display = "none";
//     }
//   }
// }

// document
//   .getElementById("departure")
//   .addEventListener("input", filterDisplayedFlights);

// // document.getElementById("destination").addEventListener("input", fetchFlights);

// // function fetchFlights() {
// //   const departureCity = document.getElementById("departure").value;
// //   const arrivalCity = document.getElementById("destination").value;

// //   console.log(departureCity);
// //   console.log(arrivalCity);

// //   // Ensure both fields have some value before making the request
// //   if (departureCity || arrivalCity) {
// //     fetch(
// //       `http://127.0.0.1:8000/flights/flight/search/?departure_city=${departureCity}&arrival_city=${arrivalCity}`
// //     )
// //       .then((response) => response.json())
// //       .then((data) => {
// //         const resultsContainer = document.getElementById("unique-container");
// //         resultsContainer.innerHTML = ""; // Clear previous results

// //         if (data.length === 0) {
// //           resultsContainer.innerHTML = "<p>No flights found</p>";
// //           return;
// //         }

// //         // Dynamically populate results
// //         data.forEach((flight) => {
// //           const flightElement = `
// //                     <div>
// //                         <h3>${flight.flight_number}: ${
// //             flight.departure_city
// //           } to ${flight.arrival_city}</h3>
// //                         <p>Departure: ${new Date(
// //                           flight.departure_time
// //                         ).toLocaleString()}</p>
// //                         <p>Arrival: ${new Date(
// //                           flight.arrival_time
// //                         ).toLocaleString()}</p>
// //                         <p>Price: $${flight.price}</p>
// //                         <p>Available Seats: ${flight.available_seats}</p>
// //                     </div>
// //                 `;
// //           resultsContainer.innerHTML += flightElement;
// //         });
// //       })
// //       .catch((error) => console.error("Error fetching flights:", error));
// //   }
// // }
