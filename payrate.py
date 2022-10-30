def computepay (h, r):
    if h <= 40:
        p = (r * h)
    elif h > 40:
        p = (r * 40 + ((h-40) * (1.5 * r))   

h = float(input("Enter Hours:"))

r = float(input("Enter Pay:"))
p = computepay(h, r)

print("Pay", p)