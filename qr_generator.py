import qrcode

def main():
    data = input("Enter the text or URL to generate QR code: ")
    img = qrcode.make(data)
    filename = input("Enter filename to save (e.g., myqr.png): ")
    img.save(filename)
    print("QR code saved as {filename}")

if __name__ == "__main__":
    main()