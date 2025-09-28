import './Card.css';

function Card({ title, description, onClick, children, className = '' }) {
  return (
    <div className={`card ${className}`} onClick={onClick}>
      {title && <h3 className="card-title">{title}</h3>}
      {description && <p className="card-description">{description}</p>}
      {children}
    </div>
  );
}

export default Card;