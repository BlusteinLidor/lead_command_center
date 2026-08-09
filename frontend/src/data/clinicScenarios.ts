import type { LeadWebhookPayload } from "../types/lead";

export interface ClinicScenario {
  id: string;
  labelEn: string;
  labelHe: string;
  payload: LeadWebhookPayload;
}

export const HEBREW_CLINIC_SCENARIOS: ClinicScenario[] = [
  {
    id: "he-urgent-fever",
    labelEn: "Urgent fever — same-day appointment",
    labelHe: "חום דחוף — תור להיום",
    payload: {
      message:
        "שלום, יש לי חום גבוה ושיעול כבר יומיים. אפשר תור לרופא משפחה היום במרפאת שקד?",
      source: "whatsapp",
      channel: "chat",
      name: "עדי מזרחי",
      phone: "+972-50-7002001",
    },
  },
  {
    id: "he-blood-test",
    labelEn: "Blood tests pricing inquiry",
    labelHe: "שאלה על מחיר בדיקות דם",
    payload: {
      message:
        "ראיתי באתר שאתם עושים בדיקות דם בבוקר. כמה זה עולה בלי הפניה ומתי יש תורים?",
      source: "webform",
      channel: "contact",
      name: "יעל שרון",
      email: "yael.sharon.demo@example.co.il",
      phone: "+972-54-7002002",
    },
  },
  {
    id: "he-new-family",
    labelEn: "New family — pediatric doctor",
    labelHe: "משפחה חדשה — רופא ילדים",
    payload: {
      message:
        "עברנו לשכונה ומחפשים רופא ילדים קבוע במרפאה. יש מקום למשפחה עם שני ילדים?",
      source: "facebook",
      channel: "lead_ad",
      name: "אורי ונועה",
      phone: "+972-52-7002003",
    },
  },
  {
    id: "he-nutrition",
    labelEn: "Nutrition consult after Instagram",
    labelHe: "ייעוץ תזונה בעקבות אינסטגרם",
    payload: {
      message:
        "היי, ראיתי סטורי על ייעוץ תזונה. יש דיאטנית במרפאת שקד? מחיר מפגש ראשון?",
      source: "instagram",
      channel: "dm",
      name: "נועה אלון",
      phone: "+972-58-7002004",
    },
  },
];

export const ENGLISH_CLINIC_SCENARIOS: ClinicScenario[] = [
  {
    id: "en-pediatric",
    labelEn: "Pediatric checkup — new patient",
    labelHe: "בדיקת ילדים — מטופל חדש",
    payload: {
      message:
        "Looking for a pediatric checkup for my 3-year-old at Almond Family Clinic. Do you accept new patients next week?",
      source: "webform",
      channel: "contact",
      name: "Emma Lang",
      email: "emma.lang.demo@example.com",
      phone: "+972-50-7003001",
    },
  },
  {
    id: "en-physio",
    labelEn: "Post-surgery physiotherapy callback",
    labelHe: "פיזיותרפיה אחרי ניתוח — חזרה",
    payload: {
      message:
        "Please call me back about physiotherapy after knee surgery. My insurance covers part of the sessions.",
      source: "phone",
      channel: "callback_request",
      name: "Mark Ezra",
      phone: "+972-52-7003002",
    },
  },
  {
    id: "en-derm",
    labelEn: "Same-week dermatology for rash",
    labelHe: "דרמטולוגיה באותו שבוע — פריחה",
    payload: {
      message:
        "Need a same-week dermatology consult for a rash on my arm. Can you send available slots?",
      source: "whatsapp",
      channel: "chat",
      name: "Sara Quinn",
      email: "sara.quinn.demo@example.com",
      phone: "+972-54-7003003",
    },
  },
  {
    id: "en-corporate",
    labelEn: "Corporate periodic checkups quote",
    labelHe: "הצעת מחיר לבדיקות תקופתיות לחברה",
    payload: {
      message:
        "We need a quote for annual employee checkups for a small company of 15 people. Are bulk packages available?",
      source: "email",
      channel: "inbound",
      name: "Jordan Pike",
      email: "jordan.pike.demo@example.com",
    },
  },
];
