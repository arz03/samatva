import uuid
from django.db import models
import random


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active_team = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        if not self.card_set.all():
            cards, active_team = self.build_board()
            self.active_team = active_team
            super().save(*args, **kwargs)
            for card in cards:
                new_card = Card(game=self, word=card["word"], team=card["team"])
                new_card.save()
            game_tracker, created = Count.objects.get_or_create(defaults={'games_played': 0})
            game_tracker.games_played += 1
            game_tracker.save()
        else:
            super().save(*args, **kwargs)

    def build_board(self):
        word_list = ['Appeal', 'Arbitration', 'Assets', 'Audit', 'Authority', 'Bail', 'Benchmark', 'Boundary', 'Brief', 'Budget', 'Bureaucracy', 'Bylaw', 'Cabinet', 'Candidature', 'Case', 'Cause', 'Certificate', 'Charter', 'Citizenship', 'Clause', 'Code', 'Commerce', 'Commission', 'Committee', 'Compliance', 'Compromise', 'Confederation', 'Consent', 'Conspiracy', 'Contract', 'Convention', 'Copyright', 'Counsel', 'Covenant', 'Custody', 'Debt', 'Decree', 'Default', 'Defendant', 'Delegation', 'Delinquent', 'Demand', 'Democracy', 'Denial', 'Dependency', 'Deportation', 'Detention', 'Discipline', 'Disclaimer', 'Discovery', 'Discretion', 'Dispute', 'Dissent', 'Docket', 'Domain', 'Duty', 'Edict', 'Efficiency', 'Election', 'Eligibility', 'Emancipation', 'Embargo', 'Enactment', 'Enforcement', 'Equity', 'Escrow', 'Ethics', 'Eviction', 'Exclusion', 'Exemption', 'Expulsion', 'Extradition', 'Federalism', 'Federation', 'Felony', 'Fiat', 'Fiduciary', 'Foreclosure', 'Forfeiture', 'Franchise', 'Fraud', 'Garnishment', 'Governing', 'Grant', 'Grievance', 'Guarantee', 'Guardian', 'Hearing', 'Heresy', 'Immunity', 'Incarceration', 'Incompetence', 'Indemnity', 'Indictment', 'Injunction', 'Inquiry', 'Insider', 'Interrogation', 'Interpretation', 'Intervention', 'Judgment', 'Judiciary', 'Jurisdiction', 'Jury', 'Justice', 'Landmark', 'Legality', 'Legislation', 'Liability', 'Libel', 'Lien', 'Limitation', 'Litigation', 'Magistrate', 'Mandate', 'Manifesto', 'Mediation', 'Minority', 'Mitigation', 'Motion', 'Negligence', 'Nomination', 'Oath', 'Obligation', 'Offence', 'Omission', 'Opinion', 'Order', 'Ordinance', 'Ownership', 'Panel', 'Parliament', 'Partition', 'Partnership', 'Patent', 'Pension', 'Plea', 'Plenary', 'Pledge', 'Precedent', 'Preemption', 'Privilege', 'Probation', 'Procedure', 'Proclamation', 'Prohibition', 'Property', 'Prosecution', 'Protocol', 'Provision', 'Quarantine', 'Quorum', 'Rebuttal', 'Recognition', 'Redress', 'Referendum', 'Reform', 'Regime', 'Regulation', 'Remand', 'Reparation', 'Repeal', 'Representation', 'Republican', 'Requisition', 'Resolution', 'Restitution', 'Sanction', 'Sovereignty', 'Statute', 'Subpoena', 'Summary', 'Summons', 'Supervision', 'Supplement', 'Suspension', 'Treaty', 'Tribunal', 'Trustee', 'Unanimity', 'Usurpation', 'Validation', 'Variance', 'Verdict', 'Waiver', 'Warrant', 'Witness', 'Writ', 'Yield', 'Abandonment', 'Abatement', 'Absenteeism', 'Abolition', 'Abridgment', 'Abscond', 'Acquisition', 'Adjudication', 'Adjournment', 'Advocate', 'Affidavit', 'Affirmation', 'Agency', 'Aggression', 'Agreement', 'Alienation', 'Allocation', 'Allegation', 'Amicus', 'Annexation', 'Antitrust', 'Appellate', 'Arraignment', 'Asset', 'Assignment', 'Assumption', 'Attachment', 'Attorney', 'Bailment', 'Bankruptcy', 'Bar', 'Bequest', 'Bill', 'Breach', 'Broker', 'Canon', 'Casework', 'Causation', 'Certification', 'Civil', 'Claim', 'Clarification', 'Clause', 'Codicil', 'Cohabitation', 'Colony', 'Commonwealth', 'Compensation', 'Competency', 'Concurrence', 'Condemnation', 'Condonation', 'Confession', 'Confidentiality', 'Confiscation', 'Constituency', 'Construction', 'Contractual', 'Conveyance', 'Conviction', 'Cooperation', 'Coordination', 'Council', 'Counsel', 'Counterclaim', 'Court', 'Creditor', 'Culmination', 'Custom', 'Custodian', 'Decency', 'Declaration', 'Deed', 'Defamation', 'Default', 'Defendant', 'Delegation', 'Deliberation', 'Delivery', 'Demurrer', 'Deportation', 'Deposition', 'Descendant', 'Determination', 'Dictum', 'Diligence', 'Disbarment', 'Discretion', 'Disenfranchisement', 'Discovery', 'Dismissal', 'Disposal', 'Dissolution', 'Document', 'Domination', 'Drafting', 'Duty', 'Elucidation', 'Empowerment', 'Endorsement', 'Entitlement', 'Enquiry', 'Escrow', 'Estoppel', 'Ethics', 'Evasion', 'Evidence', 'Exception', 'Execution', 'Executive', 'Exemption', 'Expropriation', 'Extortion', 'Facilitation', 'Filing', 'Fraudulent', 'Gains', 'Goodwill', 'Governance', 'Grounds', 'Guarantor', 'Guilty', 'Harassment', 'Hindrance', 'Honorarium', 'Hostile', 'Impeachment', 'Impediment', 'Implementation', 'Imprisonment', 'Impropriety', 'Inadmissible', 'Inauguration', 'Indictment', 'Inheritance', 'Insolvency', 'Insubordination', 'Intention', 'Interdict', 'Interlocutory', 'International', 'Intimidation', 'Inventory', 'Judicial', 'Juror', 'Jurisprudence', 'Justice', 'Justification', 'Legislature', 'Leniency', 'Liability', 'Lien', 'Liquidation', 'Lobby', 'Malfeasance', 'Mandamus', 'Manifest', 'Marginalization', 'Materiality', 'Mediation', 'Memo', 'Merger', 'Misconduct', 'Misdemeanor', 'Monetary', 'Neglect', 'Nominee', 'Nullification', 'Oath', 'Objection', 'Obligation', 'Occupant', 'Offender', 'Onus', 'Opposition', 'Overt', 'Parole', 'Partisan', 'Patent', 'Penal', 'Perjury', 'Petition', 'Plaintiff', 'Plea', 'Posthumous', 'Power', 'Precedent', 'Preclusion', 'Preference', 'Prejudice', 'Preservation', 'Presumption', 'Prevailing', 'Privilege', 'Proactive', 'Probate', 'Proceeds', 'Proclamation', 'Proctor', 'Production', 'Professionalism', 'Property', 'Prosecutor', 'Provision', 'Punitive', 'Quasi', 'Ratification', 'Reaffirmation', 'Reasonable', 'Rebuttal', 'Recognition', 'Recompense', 'Reconsideration', 'Recrimination', 'Redaction', 'Redundancy', 'Rehabilitation', 'Rejoinder', 'Relevance', 'Remittance', 'Remorse', 'Repeal', 'Replication', 'Reprieve', 'Rescindment', 'Restitution', 'Restructuring', 'Retainer', 'Revenge', 'Revocation', 'Sanction', 'Schedule', 'Scrutiny', 'Sealed', 'Sedition', 'Seizure', 'Settlement', 'Shareholder', 'Slander', 'Solvency', 'Specification', 'Stipulation', 'Subcontract', 'Subordination', 'Subrogation', 'Subsequent', 'Subsidiary', 'Summation', 'Surveillance', 'Survivorship', 'Syndicate', 'Tenant', 'Termination', 'Territorial', 'Testamentary', 'Testator', 'Tort', 'Transfer', 'Transparency', 'Trust', 'Unanimity', 'Undertaking', 'Unlawful', 'Usufruct', 'Verdict', 'Vesting', 'Vicarious', 'Voidable', 'Waiver', 'Warrant', 'Witness', 'Writ', 'Yield', 'Preamble', 'Sovereign', 'Secular', 'Republic', 'Fundamental', 'Directive', 'Amendment', 'Jurisdiction', 'Writ', 'Habeas', 'Mandamus', 'Quo', 'Prohibition', 'Certiorari', 'Separation', 'Concurrent', 'Union', 'State', 'Residual', 'Duties', 'Equality', 'Untouchability', 'Speech', 'Assembly', 'Association', 'Cultural', 'Protection', 'Liberty', 'Remedies', 'Litigation', 'Election', 'Legislative', 'Ordinance', 'Finance', 'Territories', 'Rajya', 'Lok', 'Bicameral', 'Transferable', 'Ballot', 'Impeachment', 'Joint', 'Money', 'Appropriation', 'Account', 'Credit', 'Consolidated', 'Contingency', 'Emergency', 'Review', 'Pardon', 'Federal', 'Governor', 'Cabinet', 'Quorum', 'Adjournment', 'Privilege', 'Committee', 'Constitutional', 'Statutory', 'Attorney', 'Comptroller', 'National', 'State', 'Financial', 'Violation', 'Doctrine', 'Activism', 'Privileges', 'Discretion', 'Oath', 'Defection', 'Powers', 'Council', 'Inter-State', 'Proportional', 'Representation', 'Ministerial', 'Confidence', 'Promulgation', 'Petition', 'Original', 'Appellate', 'Advisory', 'Breach', 'Concurrent', 'Separation', 'Disqualification', 'Interpretation', 'Provisions', 'Federalism', 'Directive', 'Ombudsman', 'Pension', 'Chief', 'Appointment', 'Parliamentary', 'Sessions', 'Committee', 'Speaker']


        # Create list of teams
        team1 = random.choice(["red", "blue"])
        team2 = "red" if team1 == "blue" else "blue"

        teams = [team1] * 9
        teams.extend([team2] * 8)
        teams.extend(["none"] * 7)
        teams.extend(["assassin"])

        # Shuffle list of teams
        teams_remaining = len(teams)
        while teams_remaining:
            teams_remaining -= 1
            index = random.randint(0, teams_remaining)
            teams[index], teams[teams_remaining] = teams[teams_remaining], teams[index]

        # Randomly select words from list
        words = []
        while len(words) < 25:
            word = word_list[random.randint(0, len(word_list) - 1)]
            if word not in words:
                words.append(word)

        # Assign team to card
        cards = [{"word": word, "team": team} for word, team in zip(words, teams)]

        return cards, team1


class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    word = models.CharField(max_length=75, blank=False)
    team = models.CharField(max_length=20, blank=False)
    clicked = models.BooleanField(default=False)

    def set_true(self):
        if not self.clicked:
            self.clicked = True
            self.save()

    def __str__(self):
        return self.word

    class Meta:
        ordering = ["pk"]


class Count(models.Model):
    games_played = models.IntegerField(default=0)

    def __str__(self):
        return str(self.games_played)

