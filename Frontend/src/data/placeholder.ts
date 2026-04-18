import { topic as italianArtistsTopic, options as italianArtistsOptions } from "./topics/italianArtists";
import { topic as usPresidentsTopic,   options as usPresidentsOptions }   from "./topics/usPresidents";
import { topic as rhonJTopic,          options as rhonJOptions }          from "./topics/rhonj";

const TOPICS = [
  { topic: italianArtistsTopic, options: italianArtistsOptions },
  { topic: usPresidentsTopic,   options: usPresidentsOptions },
  { topic: rhonJTopic,          options: rhonJOptions },
];

const dayIndex    = Math.floor(Date.now() / 86400000) % TOPICS.length;
const { topic, options } = TOPICS[dayIndex];

export const todaysTopic = topic;
export const allOptions  = options;

const answerIndex = Math.floor(Date.now() / 86400000) % options.length;
export const ANSWER = options[answerIndex].name;
