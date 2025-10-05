// API service for connecting to Flask backend
// TODO: Replace with your actual Flask backend URL
const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  // Passengers
  getPassengers: async () => {
    const response = await fetch(`${API_BASE_URL}/passengers`);
    return response.json();
  },
  
  createPassenger: async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/passengers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  updatePassenger: async (id: number, data: any) => {
    const response = await fetch(`${API_BASE_URL}/passengers/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  deletePassenger: async (id: number) => {
    const response = await fetch(`${API_BASE_URL}/passengers/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  // Cards
  getCards: async () => {
    const response = await fetch(`${API_BASE_URL}/cards`);
    return response.json();
  },
  
  createCard: async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/cards`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  updateCard: async (id: number, data: any) => {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  deleteCard: async (id: number) => {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  // Stations
  getStations: async () => {
    const response = await fetch(`${API_BASE_URL}/stations`);
    return response.json();
  },
  
  createStation: async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/stations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  updateStation: async (id: number, data: any) => {
    const response = await fetch(`${API_BASE_URL}/stations/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  deleteStation: async (id: number) => {
    const response = await fetch(`${API_BASE_URL}/stations/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  // Trips
  getTrips: async () => {
    const response = await fetch(`${API_BASE_URL}/trips`);
    return response.json();
  },

  // Transactions
  getTransactions: async () => {
    const response = await fetch(`${API_BASE_URL}/transactions`);
    return response.json();
  },

  // Fare Rules
  getFareRules: async () => {
    const response = await fetch(`${API_BASE_URL}/fare-rules`);
    return response.json();
  },
  
  createFareRule: async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/fare-rules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  updateFareRule: async (id: number, data: any) => {
    const response = await fetch(`${API_BASE_URL}/fare-rules/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  deleteFareRule: async (id: number) => {
    const response = await fetch(`${API_BASE_URL}/fare-rules/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  // Card Types
  getCardTypes: async () => {
    const response = await fetch(`${API_BASE_URL}/card-types`);
    return response.json();
  },
  
  createCardType: async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/card-types`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  updateCardType: async (id: number, data: any) => {
    const response = await fetch(`${API_BASE_URL}/card-types/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  deleteCardType: async (id: number) => {
    const response = await fetch(`${API_BASE_URL}/card-types/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },
};
