# Resources

Each filing family is an attribute on the client (`client.insiders`,
`client.filings`, ...). List methods return one raw page as a dict; the
`iter*()` variants follow pagination and yield rows. See the
[pagination guide](../guides/pagination.md) for how the two relate.

## Master index

::: py3spread.resources.Filings

## Insiders (Forms 3, 4, 5)

::: py3spread.resources.Insiders

## Institutional holdings (13F)

::: py3spread.resources.InstitutionalHoldings

## Private offerings (Form D)

::: py3spread.resources.PrivateOfferings

## Fund portfolios (N-PORT)

::: py3spread.resources.FundPortfolios

## Beneficial ownership (13D/13G)

::: py3spread.resources.BeneficialOwnership

## Proposed sales (Form 144)

::: py3spread.resources.ProposedSales

## Fund census (N-CEN)

::: py3spread.resources.FundCensus

## Money market funds (N-MFP)

::: py3spread.resources.MoneyMarketFunds

## Proxy votes (N-PX)

::: py3spread.resources.ProxyVotes

## Reg A+ offerings

::: py3spread.resources.RegAOfferings

## Registration statements

::: py3spread.resources.RegistrationStatements

## Entities

::: py3spread.resources.Entities

## Coverage

::: py3spread.resources.Coverage

## Changes

::: py3spread.resources.Changes
