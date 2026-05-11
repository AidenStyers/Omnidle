import type { Topic, Option } from '../types'

export const topic: Topic = {
  id: 'italian-artists',
  name: 'Best-Selling Italian Artists',
  description: 'Guess the best-selling Italian music artist!',
  attributes: ['Region', 'Period Active', 'Genre', 'Est. Sales'],
}

export const options: Option[] = [
  {
    name: 'Andrea Bocelli',
    Region: 'Tuscany',
    'Period Active': '1994–present',
    Genre: 'Operatic pop',
    'Est. Sales': '90M',
  },
  {
    name: 'Milva',
    Region: 'Emilia-Romagna',
    'Period Active': '1958–2012',
    Genre: 'Pop / Tango',
    'Est. Sales': '80M',
  },
  {
    name: 'Umberto Tozzi',
    Region: 'Piedmont',
    'Period Active': '1968–present',
    Genre: 'Pop rock',
    'Est. Sales': '75M',
  },
  {
    name: 'Ennio Morricone',
    Region: 'Lazio',
    'Period Active': '1946–2020',
    Genre: 'Soundtracks',
    'Est. Sales': '70M',
  },
  {
    name: 'Laura Pausini',
    Region: 'Emilia-Romagna',
    'Period Active': '1993–present',
    Genre: 'Pop',
    'Est. Sales': '70M',
  },
  {
    name: 'Raffaella Carrà',
    Region: 'Emilia-Romagna',
    'Period Active': '1964–2021',
    Genre: 'Disco / Pop',
    'Est. Sales': '60M',
  },
  {
    name: 'Claudio Baglioni',
    Region: 'Lazio',
    'Period Active': '1964–present',
    Genre: 'Light pop',
    'Est. Sales': '60M',
  },
  {
    name: 'Domenico Modugno',
    Region: 'Apulia',
    'Period Active': '1953–1993',
    Genre: 'Canzone',
    'Est. Sales': '60M',
  },
  {
    name: 'Eros Ramazzotti',
    Region: 'Lazio',
    'Period Active': '1981–present',
    Genre: 'Pop rock',
    'Est. Sales': '60M',
  },
  {
    name: 'Zucchero',
    Region: 'Emilia-Romagna',
    'Period Active': '1970–present',
    Genre: 'Blues / Pop',
    'Est. Sales': '60M',
  },
  {
    name: 'Edoardo Vianello',
    Region: 'Lazio',
    'Period Active': '1957–present',
    Genre: 'Pop / Twist',
    'Est. Sales': '50M',
  },
  {
    name: 'Lucio Dalla',
    Region: 'Emilia-Romagna',
    'Period Active': '1962–2012',
    Genre: 'Pop / Jazz',
    'Est. Sales': '50M',
  },
  {
    name: 'Gianni Morandi',
    Region: 'Emilia-Romagna',
    'Period Active': '1962–present',
    Genre: 'Light pop',
    'Est. Sales': '50M',
  },
  {
    name: 'Rita Pavone',
    Region: 'Piedmont',
    'Period Active': '1962–present',
    Genre: 'Pop',
    'Est. Sales': '50M',
  },
]
