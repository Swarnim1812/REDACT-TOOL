import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
    Encoding,
    PrivateFormat,
    PublicFormat,
    NoEncryption
)
import PyPDF2


class PDFSigner:
    def _init_(self, private_key_path=None, public_key_path=None):
        """
        Initialize PDFSigner with optional private and public key paths.
        If no keys exist, generate a new key pair.
        """
        if private_key_path and public_key_path:
            # Load existing keys
            with open(private_key_path, 'rb') as private_file:
                self.private_key = load_pem_private_key(private_file.read(), password=None)
            with open(public_key_path, 'rb') as public_file:
                self.public_key = load_pem_public_key(public_file.read())
        else:
            # Generate new key pair
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.public_key = self.private_key.public_key()

            # Save keys if paths not provided
            os.makedirs('keys', exist_ok=True)
            private_key_path = 'keys/private_key.pem'
            public_key_path = 'keys/public_key.pem'

            # Save private key
            with open(private_key_path, 'wb') as f:
                f.write(self.private_key.private_bytes(
                    encoding=Encoding.PEM,
                    format=PrivateFormat.PKCS8,
                    encryption_algorithm=NoEncryption()
                ))

            # Save public key
            with open(public_key_path, 'wb') as f:
                f.write(self.public_key.public_bytes(
                    encoding=Encoding.PEM,
                    format=PublicFormat.SubjectPublicKeyInfo
                ))

            print(f"New key pair generated and saved at {private_key_path} and {public_key_path}")

    def calculate_pdf_hash(self, pdf_path):
        """
        Calculate SHA-256 hash of PDF content.

        :param pdf_path: Path to the PDF file
        :return: Bytes of the PDF hash
        """
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            # Hash entire PDF content
            hash_obj = hashlib.sha256()

            for page in pdf_reader.pages:
                # Include page text in hash calculation
                text = page.extract_text()
                hash_obj.update(text.encode('utf-8'))

            return hash_obj.digest()

    def sign_pdf(self, pdf_path, signed_pdf_path):
        """
        Sign a PDF by calculating its hash and creating a signature.

        :param pdf_path: Path to the input PDF
        :param signed_pdf_path: Path to save the signed PDF
        """
        # Calculate PDF hash
        pdf_hash = self.calculate_pdf_hash(pdf_path)

        # Create signature
        signature = self.private_key.sign(
            pdf_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Read original PDF
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()

            # Copy all pages
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Add signature as a custom metadata
            pdf_writer.add_metadata({
                '/Signature': signature.hex(),
                '/HashAlgorithm': 'SHA-256'
            })

            # Write signed PDF
            with open(signed_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)

        print(f"PDF signed and saved to {signed_pdf_path}")

    def verify_pdf(self, pdf_path):
        """
        Verify PDF signature by comparing calculated hash with stored signature.

        :param pdf_path: Path to the PDF to verify
        :return: Boolean indicating verification status
        """
        try:
            # Read PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata

                # Extract signature and hash algorithm from metadata
                if not metadata or '/Signature' not in metadata:
                    print("No signature found in the PDF.")
                    return False

                # Convert hex signature back to bytes
                stored_signature = bytes.fromhex(metadata['/Signature'])

                # Calculate current PDF hash
                current_hash = self.calculate_pdf_hash(pdf_path)

                try:
                    # Verify signature
                    self.public_key.verify(
                        stored_signature,
                        current_hash,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    print("PDF signature verified successfully!")
                    return True

                except Exception as e:
                    print(f"Signature verification failed: {e}")
                    return False

        except Exception as e:
            print(f"Error during PDF verification: {e}")
            return False


# Example usage
def main():
    # Create a PDF signer
    pdf_signer = PDFSigner()

    # Sign a PDF
    pdf_signer.sign_pdf('original.pdf', 'signed.pdf')

    # Verify the signed PDF
    is_verified = pdf_signer.verify_pdf('signed.pdf')

    print(f"PDF Verification Result: {is_verified}")


if __name__ == "_main_":
    main()

# Requirements:
# pip install cryptography PyPDF2