import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from "recharts";


const COLORS = [
  "#2563eb",
  "#7c3aed",
  "#059669",
  "#d97706",
  "#dc2626",
  "#0891b2"
];


function SegmentChart({
  data = []
}) {

  return (

    <div className="chart-card">

      <div className="chart-header">

        <div>

          <h3>
            Customer Segments
          </h3>

          <p>
            Customer distribution by segment
          </p>

        </div>

      </div>


      <div className="chart-container">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <PieChart>

            <Pie

              data={data}

              dataKey="customers"

              nameKey="segment"

              cx="50%"

              cy="45%"

              outerRadius={100}

              innerRadius={55}

              paddingAngle={3}

            >

              {data.map(
                (_, index) => (

                  <Cell
                    key={`cell-${index}`}
                    fill={
                      COLORS[
                        index %
                        COLORS.length
                      ]
                    }
                  />

                )
              )}

            </Pie>


            <Tooltip />


            <Legend
              verticalAlign="bottom"
              height={36}
            />

          </PieChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}


export default SegmentChart;