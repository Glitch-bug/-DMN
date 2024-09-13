import traceback
from rest_framework.response import Response
from account.models import Address, UserBase
from rest_framework import status
from store.models import Product

def handle_exception(exception):
    if isinstance(exception, UserBase.DoesNotExist):
        print(exception)
        traceback.print_exc()
        return Response({"message":"This user does not exist"}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exception, Product.DoesNotExist):
        print(exception)
        traceback.print_exc()
        return Response({'message': "This product is not in stock"}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exception, Address.DoesNotExist):
        print(exception)
        traceback.print_exc()
        return Response({'message': "This user has no matching address"}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exception, KeyError) :
        print(exception)
        traceback.print_exc()
        return Response({"message": "Bad Request: Missing required parameters.", "details": f"The parameter {exception} is required but was not provided."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        print(type(exception))
        print(exception)
        traceback.print_exc()
        return Response({"message":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)