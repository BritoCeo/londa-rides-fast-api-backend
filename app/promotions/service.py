from datetime import datetime
from typing import Dict, Any
from app.core.firebase import get_firestore
from fastapi import HTTPException, status
from app.core.logging import logger
import uuid

class PromotionService:
    @staticmethod
    async def apply_promotion(user_uid: str, code: str) -> Dict[str, Any]:
        """Validate and apply a promotion or discount code for a user"""
        try:
            db = get_firestore()
            now = datetime.utcnow()
            discount_amount = 0
            code = code.upper()

            # For demonstration, hardcode some promo logic, 
            # ideally this would query a 'promotions' collection
            if code == "STUDENT2025":
                discount_amount = 5.0  # e.g., NAD 5 off
            else:
                # Check if it's a valid referral code
                users_ref = db.collection('users').where('referralCode', '==', code).limit(1).get()
                if not users_ref:
                    raise ValueError(f"Invalid promotion or referral code: {code}")
                # Referral code is valid, e.g. gives NAD 10 discount or 1 free ride
                # Ensure the user isn't using their own code
                if users_ref[0].id == user_uid:
                    raise ValueError("You cannot use your own referral code")
                discount_amount = 13.0  # 1 free ride (NAD 13)

            # Check if user already applied this promo to prevent multiple uses
            user_promos_ref = db.collection('users').document(user_uid).collection('applied_promos').document(code)
            if user_promos_ref.get().exists:
                raise ValueError("Promotion code already applied")

            # Apply it
            repo_data = {
                "code": code,
                "discountAmount": discount_amount,
                "appliedAt": now
            }
            user_promos_ref.set(repo_data)
            
            repo_data['appliedAt'] = repo_data['appliedAt'].isoformat()
            repo_data['message'] = "Promotion applied successfully"
            
            return repo_data
            
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.error(f"Error applying promotion: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to apply promotion")

    @staticmethod
    async def get_referral_code(user_uid: str) -> Dict[str, Any]:
        """Get or generate the user's referral code"""
        try:
            db = get_firestore()
            user_ref = db.collection('users').document(user_uid)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                raise ValueError("User not found")
                
            user_data = user_doc.to_dict()
            ref_code = user_data.get('referralCode')
            
            if not ref_code:
                # Generate new referral code
                first_name = user_data.get('firstName') or ''
                name = first_name.upper()[:3]
                if not name:
                    name = "REF"
                ref_code = f"{name}{uuid.uuid4().hex[:4].upper()}"
                user_ref.update({"referralCode": ref_code})
                
            return {
                "referralCode": ref_code,
                "message": "Share this code to get a free ride"
            }
            
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            logger.error(f"Error retrieving referral code: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve referral code")
