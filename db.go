package rvasp

import (
	"time"

	"github.com/jinzhu/gorm"
	"github.com/shopspring/decimal"
)

// VASP is a record of known partner VASPs and caches TRISA protocol information. This
// table also contains IVMS101 data that identifies the VASP.
// TODO: modify VASP ID to a GUID
type VASP struct {
	gorm.Model
	Name     string     `gorm:"uniqueIndex;size:255;not null"`
	URL      *string    `gorm:"null"`
	Country  *string    `gorm:"null"`
	Endpoint *string    `gorm:"null"`
	PubKey   *string    `gorm:"null"`
	NotAfter *time.Time `gorm:"null"`
	IsLocal  bool       `gorm:"default:false"`
	IVMS101  string     `gorm:"not null"`
}

// TableName explicitly defines the name of the table for the model
func (VASP) TableName() string {
	return "vasps"
}

// Wallet is a mapping of wallet IDs to VASPs to determine where to send transactions.
// It also contains the IVMS 101 data for KYC verification, in this table it is just
// stored as a JSON string rather than breaking it down to the field level.
type Wallet struct {
	gorm.Model
	Address    string `gorm:"uniqueIndex"`
	Email      string `gorm:"uniqueIndex"`
	ProviderID uint   `gorm:"not null"`
	Provider   VASP   `gorm:"foreignKey:ProviderID"`
	IVMS101    string `gorm:"not null"`
}

// TableName explicitly defines the name of the table for the model
func (Wallet) TableName() string {
	return "wallets"
}

// Account contains details about the transactions that are served by the local VASP.
type Account struct {
	gorm.Model
	Name          string          `gorm:"not null"`
	Email         string          `gorm:"uniqueIndex;not null"`
	WalletAddress string          `gorm:"uniqueIndex;not null;column:wallet_address"`
	Wallet        Wallet          `gorm:"foreignKey:WalletAddress"`
	Balance       decimal.Decimal `gorm:"type:numeric(15,2)"`
	Completed     uint64          `gorm:"not null"`
	Pending       uint64          `gorm:"not null"`
}

// TableName explicitly defines the name of the table for the model
func (Account) TableName() string {
	return "accounts"
}

// Transaction holds exchange information to send money from one account to another.
type Transaction struct {
	gorm.Model
	AccountID     uint            `gorm:"not null"`
	Account       Account         `gorm:"foreignKey:AcountID"`
	OriginatorID  uint            `gorm:"not null"`
	Originator    Wallet          `gorm:"foreignKey:OriginatorID"`
	BeneficiaryID uint            `gorm:"not null"`
	Beneficiary   Wallet          `gorm:"foreignKey:BeneficiaryID"`
	Amount        decimal.Decimal `gorm:"type:numeric(15,2)"`
	Debit         bool            `gorm:"not null"`
	Completed     bool            `gorm:"not null;default:false"`
	Timestamp     time.Time       `gorm:"not null"`
}
