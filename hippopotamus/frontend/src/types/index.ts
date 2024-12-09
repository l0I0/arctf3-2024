export interface User {
  username: string;
  is_verified: boolean;
  telegram_id: string | null;
  coin_balance: number;
}

export interface ShopItem {
  id: number;
  name: string;
  description: string;
  price: number;
  content?: string;
}

export interface Purchase {
  id: number;
  item_name: string;
  description: string;
  content: string;
  purchase_date: string;
  formatted_date: string;
}

export interface TapHippoResponse {
  message: string;
  new_balance: number;
  warning?: string;
}

export interface ClickEffect {
  id: number;
  x: number;
  y: number;
  amount: number;
  opacity: number;
}

export interface Candidate {
  id: number;
  name: string;
  votes: number;
}

export interface Election {
  id: number | null;
  election_start: string | null;
  election_end: string | null;
  time_left: string | null;
  winner: Candidate | null;
  candidates: Candidate[];
} 