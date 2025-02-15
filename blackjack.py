from typing import List  # Добавляем импорт
import random

cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

def calculate_hand_value(hand: List[str]) -> int:
    value = sum(card_values[card] for card in hand)
    aces = hand.count("A")
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def deal_card() -> str:
    return random.choice(cards)

def determine_winner(user_hand: List[str], dealer_hand: List[str]) -> str:
    user_value = calculate_hand_value(user_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if user_value > 21:
        return "lose"
    if dealer_value > 21:
        return "win"
    if user_value == dealer_value:
        return "draw"
    return "win" if user_value > dealer_value else "lose"