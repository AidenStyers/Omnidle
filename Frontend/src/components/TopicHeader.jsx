export default function TopicHeader({ topic }) {
  return (
    <header className="topic-header">
      <p className="topic-label">TODAY'S TOPIC</p>
      <h1 className="topic-name">{topic.name}</h1>
      <p className="topic-desc">{topic.description}</p>
    </header>
  );
}
