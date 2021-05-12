import valideer as V
from account import account_schema

sample_schema = {
	"accounts": V.Object(account_schema)
}