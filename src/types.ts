export interface Message {
  id: string;
  sender: "user" | "bot";
  text: string;
  timestamp: string;
  suggestedReplies?: string[];
}

export interface RoiEstimate {
  monthlySavings: number;
  extraSales: number;
  hoursRegained: number;
  paybackDays: number;
}

export interface LeadFormData {
  name: string;
  phone: string;
  email: string;
  businessType: string;
  notes: string;
}

export interface ServiceDetail {
  id: string;
  title: string;
  tag: string;
  iconName: string;
  description: string;
  features: string[];
  mockupTitle: string;
  mockupSubtitle: string;
  previewType: "whatsapp" | "menu" | "portfolio" | "web";
}
