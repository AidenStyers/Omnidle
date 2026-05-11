export interface Topic {
  id: string
  name: string
  description: string
  attributes: string[]
}

export interface Option {
  name: string
  [attr: string]: string | number | boolean }



















export type HintType = "correct" | 'higher' | 'lower' | 'wrong'

export interface AttrResult {
  
  attr: string
  value: string
  hint: HintType }

export interface Guess {
  name: string
  result: AttrResult[]
}
