// Replace with real API responses when backend is ready.
// todaysTopic and allOptions will come from the backend; ANSWER will never be sent to the client.

import { topic as italianArtistsTopic, options as italianArtistsOptions } from "./topics/italianArtists";
import { topic as usPresidentsTopic, options as usPresidentsOptions } from "./topics/usPresidents";
import { topic as rhonJTopic, options as rhonJOptions } from "./topics/rhonj";

const TOPICS = [
  { topic: italianArtistsTopic, options: italianArtistsOptions },
  { topic: usPresidentsTopic,   options: usPresidentsOptions },
  { topic: rhonJTopic,          options: rhonJOptions },
];

// Rotate topic by day so each day gets a different one
const dayIndex = Math.floor(Date.now() / 86400000) % TOPICS.length;
const { topic, options } = TOPICS[dayIndex];

export const todaysTopic = topic;
export const allOptions = options;

// Pick a deterministic daily answer from the options list
const answerIndex = Math.floor(Date.now() / 86400000) % options.length;
export const ANSWER = options[answerIndex].name;
