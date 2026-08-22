function StatCard({
  title,
  value,
  subtitle,
  icon: Icon
}) {

  return (

    <div className="stat-card">

      <div className="stat-card-header">

        <span className="stat-title">
          {title}
        </span>

        {Icon && (

          <div className="stat-icon">

            <Icon
              size={19}
            />

          </div>

        )}

      </div>


      <div className="stat-value">

        {value}

      </div>


      {subtitle && (

        <div className="stat-subtitle">

          {subtitle}

        </div>

      )}

    </div>
  );
}


export default StatCard;