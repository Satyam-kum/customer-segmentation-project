import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";


function RevenueChart({
  data = []
}) {

  return (

    <div className="chart-card">

      <div className="chart-header">

        <div>

          <h3>
            Revenue Trend
          </h3>

          <p>
            Monthly revenue performance
          </p>

        </div>

      </div>


      <div className="chart-container">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <LineChart
            data={data}
            margin={{
              top: 10,
              right: 20,
              left: 0,
              bottom: 10
            }}
          >

            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey="period"
              tick={{
                fontSize: 12
              }}
            />

            <YAxis
              tick={{
                fontSize: 12
              }}
            />

            <Tooltip
              formatter={(value) =>
                `£${Number(value).toLocaleString()}`
              }
            />

            <Line
              type="monotone"
              dataKey="revenue"
              stroke="currentColor"
              strokeWidth={3}
              dot={false}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}


export default RevenueChart;