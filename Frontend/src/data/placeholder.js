// Replace with real API responses when backend is ready

export const todaysTopic = {
  id: 1,
  name: "Car Brands",
  description: "Guess today's car brand!",
  attributes: ["Country", "Founded", "Segment", "Parent Company", "Still Active"],
};

export const allOptions = [
  { name: "Toyota",    Country: "Japan",    Founded: 1937, Segment: "Mass Market", "Parent Company": "Toyota Group",    "Still Active": true },
  { name: "BMW",       Country: "Germany",  Founded: 1916, Segment: "Luxury",      "Parent Company": "BMW Group",       "Still Active": true },
  { name: "Ford",      Country: "USA",      Founded: 1903, Segment: "Mass Market", "Parent Company": "Ford Motor Co.",  "Still Active": true },
  { name: "Ferrari",   Country: "Italy",    Founded: 1939, Segment: "Supercar",    "Parent Company": "Exor N.V.",       "Still Active": true },
  { name: "Pontiac",   Country: "USA",      Founded: 1926, Segment: "Mass Market", "Parent Company": "GM",              "Still Active": false },
  { name: "Volkswagen",Country: "Germany",  Founded: 1937, Segment: "Mass Market", "Parent Company": "VW Group",        "Still Active": true },
  { name: "Honda",     Country: "Japan",    Founded: 1948, Segment: "Mass Market", "Parent Company": "Honda Motor Co.", "Still Active": true },
  { name: "Lamborghini",Country:"Italy",    Founded: 1963, Segment: "Supercar",    "Parent Company": "VW Group",        "Still Active": true },
];

// The answer (backend will determine this, never sent to client in prod)
export const ANSWER = "BMW";
