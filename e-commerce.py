# Real world application using control structures
# Assignment 2: E-commerce app that calculates final price with subtotal,
# discount, coupon codes, tax rates by location, and a login system
# with three user types: Admin, Customers, and Cashiers.

# ── USER DATABASE ─────────────────────────────────
# In a real app these would be stored in a database
USERS = {
    "admin":   {"password": "admin123",    "role": "Admin"},
    "cashier": {"password": "cash456",     "role": "Cashier"},
    "quinn":   {"password": "customer789", "role": "Customer"},
}

# ── LOGIN SYSTEM ──────────────────────────────────

def login():
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        print("\n--- LOGIN ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = USERS.get(username)

        if user and user["password"] == password:
            return {"username": username, "role": user["role"]}
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Invalid credentials. {remaining} attempt(s) remaining.")

    return None


# ── ACCESS CONTROL ────────────────────────────────

def show_access_menu(user):
    role = user["role"]

    if role == "Admin":
        print("\n[Admin Panel] You have full access to all features.")
        print(" - View all orders")
        print(" - Manage users")
        print(" - Access reports")
        print(" - Process sales (checkout)")

    elif role == "Cashier":
        print("\n[Cashier Panel] You can process sales and view orders.")
        print(" - Process sales (checkout)")
        print(" - View today's orders")

    elif role == "Customer":
        print("\n[Customer Panel] You can shop and view your own orders.")
        print(" - Browse products")
        print(" - Checkout")


# ── SUBTOTAL-BASED DISCOUNT ───────────────────────

def apply_subtotal_discount(subtotal):
    if subtotal >= 1_000_000:
        print("You qualify for a VIP discount (15%)!")
        return 0.15
    elif subtotal >= 500_000:
        print("You qualify for a Gold discount (10%)!")
        return 0.10
    elif subtotal >= 200_000:
        print("You qualify for a Silver discount (5%)!")
        return 0.05
    elif subtotal >= 50_000:
        print("You qualify for a Bronze discount (2%)!")
        return 0.02
    else:
        print("No subtotal-based discount (subtotal below 50,000).")
        return 0.0


# ── COUPON CODE ───────────────────────────────────

def apply_coupon(subtotal):
    code = input("Enter coupon code (or press Enter to skip): ").strip().upper()

    if not code:
        print("No coupon applied.")
        return 0.0
    elif code == "SAVE10":
        discount = subtotal * 0.10
        print(f"Coupon SAVE10 applied! 10% off → -UGX {discount:,.2f}")
        return discount
    elif code == "FLAT5000":
        print("Coupon FLAT5000 applied! Flat UGX 5,000 off.")
        return 5000.0
    elif code == "NEWUSER":
        discount = subtotal * 0.15
        print(f"Coupon NEWUSER applied! 15% off for new users → -UGX {discount:,.2f}")
        return discount
    elif code == "HOLIDAY":
        discount = subtotal * 0.20
        print(f"Coupon HOLIDAY applied! 20% holiday special → -UGX {discount:,.2f}")
        return discount
    else:
        print(f'Invalid coupon code "{code}". No discount applied.')
        return 0.0


# ── TAX RATE BY LOCATION ──────────────────────────

def get_tax_rate():
    print("\nSelect your location for tax calculation:")
    print("  1. Kampala (18% VAT)")
    print("  2. Other Uganda cities (16% VAT)")
    print("  3. East Africa (EAC — 14%)")
    print("  4. International (No local tax — 0%)")
    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        print("Location: Kampala — Tax rate: 18%")
        return 0.18
    elif choice == "2":
        print("Location: Other Uganda — Tax rate: 16%")
        return 0.16
    elif choice == "3":
        print("Location: East Africa — Tax rate: 14%")
        return 0.14
    elif choice == "4":
        print("Location: International — No local tax.")
        return 0.0
    else:
        print("Invalid choice. Defaulting to Other Uganda (16%).")
        return 0.16


# ── CHECKOUT ──────────────────────────────────────

def run_checkout(user):
    print("\n========================================")
    print("              CHECKOUT                  ")
    print("========================================")

    # 1. Get subtotal
    while True:
        try:
            subtotal = float(input("Enter subtotal (UGX): ").strip())
            if subtotal > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # 2. Subtotal-based discount
    subtotal_discount_rate = apply_subtotal_discount(subtotal)
    subtotal_discount_amount = subtotal * subtotal_discount_rate
    print(f"Subtotal discount ({int(subtotal_discount_rate * 100)}%): -UGX {subtotal_discount_amount:,.2f}")

    # 3. Coupon discount
    coupon_discount = apply_coupon(subtotal)

    # 4. Price after discounts
    total_discount = subtotal_discount_amount + coupon_discount
    discounted_price = subtotal - total_discount

    # 5. Tax
    tax_rate = get_tax_rate()
    tax_amount = discounted_price * tax_rate

    # 6. Final price
    final_price = discounted_price + tax_amount

    # ── RECEIPT ──────────────────────────────────
    print("\n========================================")
    print("                RECEIPT                 ")
    print("========================================")
    print(f"Subtotal:              UGX {subtotal:>12,.2f}")
    print(f"Subtotal discount:    -UGX {subtotal_discount_amount:>12,.2f}")
    print(f"Coupon discount:      -UGX {coupon_discount:>12,.2f}")
    print(f"Price after discount:  UGX {discounted_price:>12,.2f}")
    print(f"Tax ({int(tax_rate * 100)}%):              +UGX {tax_amount:>12,.2f}")
    print("----------------------------------------")
    print(f"FINAL PRICE:           UGX {final_price:>12,.2f}")
    print("========================================")
    print(f"Served by: {user['username']} ({user['role']})")
    print("Thank you for shopping at ShopEase!")


# ── MAIN ──────────────────────────────────────────

def main():
    print("========================================")
    print("     WELCOME TO SHOPEASE E-COMMERCE     ")
    print("========================================")

    user = login()

    if user is None:
        print("Too many failed attempts. Exiting.")
        return

    print(f"\nLogin successful! Welcome, {user['username']}.")
    print(f"Role: {user['role']}")

    show_access_menu(user)
    run_checkout(user)


if __name__ == "__main__":
    main()