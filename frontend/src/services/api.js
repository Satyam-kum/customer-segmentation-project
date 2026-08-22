
import axios from "axios";


const api = axios.create({

  baseURL:
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000",

  headers: {
    "Content-Type":
      "application/json"
  }
});


/* ============================================================
   ANALYTICS
   ============================================================ */


export async function getDashboard() {

  const response =
    await api.get(
      "/analytics/dashboard"
    );

  return response.data;
}


export async function getRevenue() {

  const response =
    await api.get(
      "/analytics/revenue"
    );

  return response.data;
}


export async function getCountries() {

  const response =
    await api.get(
      "/api/analytics/countries"
    );

  return response.data;
}


export async function getTopCustomers(
  limit = 10
) {

  const response =
    await api.get(
      `/analytics/top-customers?limit=${limit}`
    );

  return response.data;
}


export async function getRetention() {

  const response =
    await api.get(
      "/analytics/retention"
    );

  return response.data;
}


export async function getRetentionBySegment() {

  const response =
    await api.get(
      "/analytics/retention-by-segment"
    );

  return response.data;
}


/* ============================================================
   CUSTOMERS
   ============================================================ */


export async function getCustomers({
  page = 1,
  pageSize = 20,
  search = "",
  segment = ""
} = {}) {

  const params = new URLSearchParams();

  params.set(
    "page",
    page
  );

  params.set(
    "page_size",
    pageSize
  );

  if (search) {

    params.set(
      "search",
      search
    );
  }

  if (segment) {

    params.set(
      "segment",
      segment
    );
  }

  const response =
    await api.get(
      `/api/customers?${params.toString()}`
    );

  return response.data;
}


export async function getCustomer(
  customerId
) {

  const response =
    await api.get(
      `/api/customers/${customerId}`
    );

  return response.data;
}


/* ============================================================
   SEGMENTATION
   ============================================================ */


export async function getSegmentSummary() {

  const response =
    await api.get(
      "/api/segmentation/summary"
    );

  return response.data;
}


export async function getSegmentDistribution() {

  const response =
    await api.get(
      "/api/segmentation/distribution"
    );

  return response.data;
}


export async function getCustomerSegment(
  customerId
) {

  const response =
    await api.get(
      `/api/segmentation/customer/${customerId}`
    );

  return response.data;
}


/* ============================================================
   CHURN
   ============================================================ */


export async function getCustomerChurn(
  customerId
) {

  const response =
    await api.get(
      `/api/churn/customer/${customerId}`
    );

  return response.data;
}


export async function getHighRiskCustomers(
  limit = 50
) {

  const response =
    await api.get(
      `/api/churn/high-risk?limit=${limit}`
    );

  return response.data;
}


/* ============================================================
   DEFAULT AXIOS INSTANCE
   ============================================================ */

export default api;