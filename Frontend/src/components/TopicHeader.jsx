export default function TopicHeader({ topic }) {
  return (
    <header className="topic-header">
      <div className="site-wordmark">OMNIDLE</div>
      <div className="topic-pill">TODAY'S TOPIC</div>
      <h1 className="topic-name">{topic.name}</h1>
      <p className="topic-desc">{topic.description}</p>
    </header>
  );
}
